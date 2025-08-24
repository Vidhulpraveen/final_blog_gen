"""
AI Service for Blog Generation
Handles topic generation, research, and content writing
"""
import asyncio
import json
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import openai
from app.core.config import settings

logger = logging.getLogger(__name__)

class AIService:
    """AI service for blog generation using multiple AI models"""
    
    def __init__(self):
        """Initialize AI service with API keys"""
        self.openai_client = None
        self.gemini_client = None
        self._initialize_clients()
    
    def _initialize_clients(self):
        """Initialize AI API clients"""
        try:
            if settings.OPENAI_API_KEY:
                self.openai_client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
                logger.info("OpenAI client initialized successfully")
            
            if settings.GEMINI_API_KEY:
                import google.generativeai as genai
                genai.configure(api_key=settings.GEMINI_API_KEY)
                self.gemini_client = genai.GenerativeModel('gemini-1.5-pro')
                logger.info("Gemini client initialized successfully")
                
        except Exception as e:
            logger.error(f"Failed to initialize AI clients: {str(e)}")
    
    async def generate_topics(self, main_topic: str, count: int = 10) -> List[Dict[str, Any]]:
        """
        Generate multiple unique blog topics from a main theme
        
        Args:
            main_topic: Main topic (e.g., "Digital Marketing")
            count: Number of topics to generate
            
        Returns:
            List of topic dictionaries with title, keywords, audience, length
        """
        try:
            prompt = f"""
            Generate {count} unique blog topics about "{main_topic}". 
            
            Requirements:
            - Each topic should be different and cover a unique angle
            - Include beginner, intermediate, and advanced topics
            - Vary the focus (strategic, tactical, tools, trends, case studies)
            - Make topics engaging and SEO-friendly
            
            For each topic, provide:
            - title: Engaging blog title
            - keywords: 5-8 relevant keywords
            - target_audience: Who this topic is for
            - content_length: "short" (500-800 words), "medium" (800-1200 words), or "long" (1200-2000 words)
            
            Return as JSON array.
            """
            
            if self.openai_client:
                response = await self._call_openai(prompt, "gpt-4")
            elif self.gemini_client:
                response = await self._call_gemini(prompt, "gemini-1.5-pro")
            else:
                # Fallback to mock data if no AI clients available
                return self._generate_mock_topics(main_topic, count)
            
            # Parse AI response
            topics = self._parse_topics_response(response, count)
            logger.info(f"Generated {len(topics)} topics for '{main_topic}'")
            return topics
            
        except Exception as e:
            logger.error(f"Failed to generate topics: {str(e)}")
            # Fallback to mock data
            return self._generate_mock_topics(main_topic, count)
    
    async def research_topic(self, topic: str) -> Dict[str, Any]:
        """
        Research a specific topic to gather information
        
        Args:
            topic: Blog topic to research
            
        Returns:
            Research data including key points, statistics, examples
        """
        try:
            prompt = f"""
            Research the topic: "{topic}"
            
            Provide comprehensive research data including:
            
            Key Points (5-7 main insights):
            - Important concepts and ideas
            - Current trends and developments
            - Best practices and strategies
            
            Statistics (3-5 relevant stats):
            - Market size and growth
            - User behavior data
            - Performance metrics
            
            Examples (2-3 real-world examples):
            - Case studies
            - Success stories
            - Industry applications
            
            Return as JSON with keys: key_points, statistics, examples
            """
            
            if self.openai_client:
                response = await self._call_openai(prompt, "gpt-4")
            elif self.gemini_client:
                response = await self._call_gemini(prompt, "gemini-1.5-pro")
            else:
                # Fallback to mock data if no AI clients available
                return self._generate_mock_research(topic)
            
            # Parse AI response
            research = self._parse_research_response(response)
            logger.info(f"Research completed for topic: {topic}")
            return research
            
        except Exception as e:
            logger.error(f"Failed to research topic '{topic}': {str(e)}")
            # Fallback to mock data
            return self._generate_mock_research(topic)
    
    async def write_blog_content(self, title: str, research: Dict[str, Any], content_length: str = "medium") -> str:
        """
        Write complete blog content based on research
        
        Args:
            title: Blog title
            research: Research data from research_topic
            content_length: "short", "medium", or "long"
            
        Returns:
            Complete HTML blog content
        """
        try:
            # Determine word count based on content length
            word_counts = {
                "short": "500-800",
                "medium": "800-1200", 
                "long": "1200-2000"
            }
            target_words = word_counts.get(content_length, "800-1200")
            
            prompt = f"""
            Write a complete blog post with the title: "{title}"
            
            Target length: {target_words} words
            
            Use this research data:
            Key Points: {research.get('key_points', [])}
            Statistics: {research.get('statistics', {})}
            Examples: {research.get('examples', [])}
            
            Requirements:
            - Write engaging, informative content
            - Include relevant statistics and examples
            - Use proper HTML formatting (h1, h2, h3, p, ul, li, strong, em)
            - Make it easy to read and scan
            - Include a compelling introduction and conclusion
            
            Return the complete blog post in HTML format.
            """
            
            if self.openai_client:
                response = await self._call_openai(prompt, "gpt-4")
            elif self.gemini_client:
                response = await self._call_gemini(prompt, "gemini-1.5-pro")
            else:
                # Fallback to mock data if no AI clients available
                return self._generate_mock_content(title, content_length)
            
            # Clean and format the response
            content = self._clean_html_content(response)
            logger.info(f"Blog content generated for: {title}")
            return content
            
        except Exception as e:
            logger.error(f"Failed to write blog content for '{title}': {str(e)}")
            # Fallback to mock data
            return self._generate_mock_content(title, content_length)
    
    async def _call_openai(self, prompt: str, model: str = "gpt-4") -> str:
        """Call OpenAI API"""
        try:
            response = self.openai_client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=4000,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API call failed: {str(e)}")
            raise
    
    async def _call_gemini(self, prompt: str, model: str = "gemini-1.5-pro") -> str:
        """Call Gemini API"""
        try:
            response = self.gemini_client.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Gemini API call failed: {str(e)}")
            raise
    
    def _parse_topics_response(self, response: str, expected_count: int) -> List[Dict[str, Any]]:
        """Parse AI response for topic generation"""
        try:
            # Try to extract JSON from response
            if "```json" in response:
                json_start = response.find("```json") + 7
                json_end = response.find("```", json_start)
                json_str = response[json_start:json_end].strip()
            elif "```" in response:
                json_start = response.find("```") + 3
                json_end = response.find("```", json_start)
                json_str = response[json_start:json_end].strip()
            else:
                json_str = response.strip()
            
            topics = json.loads(json_str)
            
            # Ensure we have the expected number of topics
            if len(topics) < expected_count:
                # Generate additional mock topics to fill the gap
                additional_topics = self._generate_mock_topics("", expected_count - len(topics))
                topics.extend(additional_topics)
            
            return topics[:expected_count]
            
        except Exception as e:
            logger.error(f"Failed to parse topics response: {str(e)}")
            return self._generate_mock_topics("", expected_count)
    
    def _parse_research_response(self, response: str) -> Dict[str, Any]:
        """Parse AI response for research data"""
        try:
            # Try to extract JSON from response
            if "```json" in response:
                json_start = response.find("```json") + 7
                json_end = response.find("```", json_start)
                json_str = response[json_start:json_end].strip()
            elif "```" in response:
                json_start = response.find("```") + 3
                json_end = response.find("```", json_start)
                json_str = response[json_start:json_end].strip()
            else:
                json_str = response.strip()
            
            return json.loads(json_str)
            
        except Exception as e:
            logger.error(f"Failed to parse research response: {str(e)}")
            return self._generate_mock_research("")
    
    def _clean_html_content(self, content: str) -> str:
        """Clean and format HTML content"""
        # Remove any markdown formatting
        content = content.replace("```html", "").replace("```", "")
        content = content.strip()
        
        # Ensure proper HTML structure
        if not content.startswith("<"):
            content = f"<p>{content}</p>"
        
        return content
    
    def _generate_mock_topics(self, main_topic: str, count: int) -> List[Dict[str, Any]]:
        """Generate mock topics for testing/fallback"""
        mock_topics = [
            {
                "title": f"{main_topic} Fundamentals: Getting Started",
                "keywords": [main_topic.lower(), "basics", "beginner", "guide"],
                "target_audience": "beginners",
                "content_length": "medium"
            },
            {
                "title": f"Advanced {main_topic} Strategies for 2024",
                "keywords": [main_topic.lower(), "advanced", "strategies", "2024"],
                "target_audience": "professionals",
                "content_length": "long"
            },
            {
                "title": f"{main_topic} Best Practices and Tips",
                "keywords": [main_topic.lower(), "best practices", "tips", "optimization"],
                "target_audience": "intermediate",
                "content_length": "medium"
            }
        ]
        
        # Generate additional topics if needed
        while len(mock_topics) < count:
            mock_topics.append({
                "title": f"{main_topic} Topic {len(mock_topics) + 1}",
                "keywords": [main_topic.lower(), f"topic{len(mock_topics) + 1}"],
                "target_audience": "general",
                "content_length": "medium"
            })
        
        return mock_topics[:count]
    
    def _generate_mock_research(self, topic: str) -> Dict[str, Any]:
        """Generate mock research data for testing/fallback"""
        return {
            "key_points": [
                f"Key point 1 about {topic}",
                f"Key point 2 about {topic}",
                f"Key point 3 about {topic}"
            ],
            "statistics": {
                "growth_rate": "15% annually",
                "market_size": "$50 billion",
                "adoption_rate": "60% of companies"
            },
            "examples": [
                f"Example company A using {topic}",
                f"Example company B implementing {topic}"
            ],
            "trends": [
                f"Trend 1 in {topic}",
                f"Trend 2 in {topic}"
            ],
            "best_practices": [
                f"Best practice 1 for {topic}",
                f"Best practice 2 for {topic}"
            ],
            "common_mistakes": [
                f"Common mistake 1 in {topic}",
                f"Common mistake 2 in {topic}"
            ]
        }
    
    def _generate_mock_content(self, topic: str, target_length: str) -> str:
        """Generate mock blog content for testing/fallback"""
        return f"""
        <h2>{topic}</h2>
        <p>This is a sample blog post about {topic}. The content would be generated by AI based on research and best practices.</p>
        
        <h3>Key Points</h3>
        <ul>
            <li>Important point 1 about {topic}</li>
            <li>Important point 2 about {topic}</li>
            <li>Important point 3 about {topic}</li>
        </ul>
        
        <h3>Conclusion</h3>
        <p>In conclusion, {topic} is an important topic that requires careful consideration and implementation.</p>
        """

# Create global instance
ai_service = AIService()
