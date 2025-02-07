from typing import List, Dict, Optional
import httpx
import json
import os
import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)
class SearchResult:
    def __init__(self, title: str, link: str, snippet: str, source: str):
        self.title = title
        self.link = link
        self.snippet = snippet
        self.source = source

    def to_dict(self) -> Dict:
        return {
            "title": self.title,
            "link": self.link,
            "snippet": self.snippet,
            "source": self.source
        }

class SearchEngine(ABC):
    @abstractmethod
    async def search(self, query: str, num_results: int = 10) -> List[SearchResult]:
        pass

class DuckDuckGoSearch(SearchEngine):
    def __init__(self):
        self.base_url = "https://api.duckduckgo.com"
        
    async def search(self, query: str, num_results: int = 10) -> List[SearchResult]:
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                params = {
                    'q': query,
                    'format': 'json',
                    'no_html': 1,
                    'no_redirect': 1,
                    't': 'D' # 使用默认主题
                }
                
                logger.info(f"Sending request to DuckDuckGo: {query}")
                logger.info(f"Request URL: {self.base_url}")
                logger.info(f"Request params: {params}")
                
                response = await client.get(self.base_url, params=params)
                logger.info(f"Response status: {response.status_code}")
                logger.info(f"Response headers: {response.headers}")
                response.raise_for_status()
                data = response.json()
                logger.info("DuckDuckGo search request successful")
            except Exception as e:
                logger.error(f"DuckDuckGo search failed: {str(e)}")
                return []
            
            results = []
            
            # 处理AbstractText作为第一个结果(如果存在)
            if data.get('AbstractText'):
                results.append(SearchResult(
                    title=data.get('Heading', ''),
                    link=data.get('AbstractURL', ''),
                    snippet=data.get('AbstractText', ''),
                    source='duckduckgo'
                ))
            
            # 处理Results字段(如果存在)
            if data.get('Results'):
                for r in data.get('Results', []):
                    if 'Text' in r and 'FirstURL' in r:
                        results.append(SearchResult(
                            title=r.get('Text', '').split(' - ')[0],
                            link=r.get('FirstURL', ''),
                            snippet=r.get('Text', ''),
                            source='duckduckgo'
                        ))
            
            # 处理相关链接
            for r in data.get('RelatedTopics', []):
                if isinstance(r, dict) and 'Topics' in r:
                    # 处理分组的主题
                    for topic in r['Topics']:
                        if 'Text' in topic and 'FirstURL' in topic:
                            results.append(SearchResult(
                                title=topic.get('Text', '').split(' - ')[0],
                                link=topic.get('FirstURL', ''),
                                snippet=topic.get('Text', ''),
                                source='duckduckgo'
                            ))
                elif isinstance(r, dict) and 'Text' in r and 'FirstURL' in r:
                    # 处理单个主题
                    results.append(SearchResult(
                        title=r.get('Text', '').split(' - ')[0],
                        link=r.get('FirstURL', ''),
                        snippet=r.get('Text', ''),
                        source='duckduckgo'
                    ))
                    
            return results[:num_results]

class GoogleSearch(SearchEngine):
    def __init__(self, api_key: str, cse_id: str):
        self.api_key = api_key
        self.cse_id = cse_id
        self.base_url = "https://www.googleapis.com/customsearch/v1"

    async def search(self, query: str, num_results: int = 10) -> List[SearchResult]:
        if not self.api_key or not self.cse_id:
            logger.warning("Google search credentials not configured")
            return []
            
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                params = {
                    'key': self.api_key,
                    'cx': self.cse_id,
                    'q': query,
                    'num': min(num_results, 10)
                }
                
                logger.info(f"Sending request to Google: {query}")
                response = await client.get(self.base_url, params=params)
                response.raise_for_status()
                data = response.json()
                logger.info("Google search request successful")
            except Exception as e:
                logger.error(f"Google search failed: {str(e)}")
                return []
            
            results = []
            for item in data.get('items', []):
                results.append(SearchResult(
                    title=item.get('title', ''),
                    link=item.get('link', ''),
                    snippet=item.get('snippet', ''),
                    source='google'
                ))
                
            return results

class SearchManager:
    def __init__(self):
        self.engines: List[SearchEngine] = []
        self._initialize_engines()
        
    def _initialize_engines(self):
        # 总是添加DuckDuckGo搜索
        self.engines.append(DuckDuckGoSearch())
        
        # 如果配置文件存在,尝试添加Google搜索
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    config = json.load(f)
                if 'google' in config:
                    google_config = config['google']
                    if google_config.get('api_key') and google_config.get('cse_id'):
                        self.engines.append(GoogleSearch(
                            api_key=google_config['api_key'],
                            cse_id=google_config['cse_id']
                        ))
            except Exception as e:
                print(f"Failed to load Google search configuration: {e}")
                
    async def search(self, query: str, num_results: int = 10, engine: str = "all") -> List[Dict]:
        all_results = []
        
        if not self.engines:
            logger.warning("No search engines available")
            return []

        logger.info(f"Starting search with query: {query}, engine: {engine}, num_results: {num_results}")
        
        for search_engine in self.engines:
            engine_name = search_engine.__class__.__name__.lower()
            if engine_name.startswith('duckduckgo'):
                engine_type = 'duckduckgo'
            elif engine_name.startswith('google'):
                engine_type = 'google'
            else:
                engine_type = engine_name
                
            if engine_type != engine.lower():
                logger.debug(f"Skipping {engine_name} as it doesn't match requested engine: {engine}")
                continue
                
            try:
                results = await search_engine.search(query, num_results)
                logger.info(f"Got {len(results)} results from {engine_name}")
                logger.info(f"Raw results: {results}")  # 添加原始结果日志
                
                # 检查结果类型
                if results:
                    logger.info(f"First result type: {type(results[0])}")
                    
                converted_results = [r.to_dict() for r in results]
                logger.info(f"Converted results: {converted_results}")  # 添加转换后结果日志
                all_results.extend(converted_results)
            except Exception as e:
                logger.error(f"Search failed for {engine_name}: {str(e)}", exc_info=True)
                
        final_results = all_results[:num_results]
        logger.info(f"Returning {len(final_results)} total results")
        return final_results