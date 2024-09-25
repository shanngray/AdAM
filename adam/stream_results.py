import logging
from contextlib import asynccontextmanager
import asyncio

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class StreamLLM:
    """
    A class to handle streaming of LLM (Language Learning Model) results.
    
    This class provides methods to initialize streaming and stream results
    from an LLM chain.
    """
    
    async def init_streaming(self):
        """
        Initialize the streaming process.
        
        This method is currently a placeholder and can be expanded to include
        any necessary setup for streaming.
        """
        print("init_streaming")
    
    async def stream_results(self, chain, input_data):
        """
        Stream results from the LLM chain.
        
        This method takes a chain and input data, processes it through the chain,
        and yields partial results as they become available.
        
        Args:
            chain: The LLM chain to process the input data.
            input_data: The input data to be processed by the chain.
        
        Yields:
            Partial results from the LLM chain.
        
        Raises:
            Exception: If an error occurs during streaming.
        """
        logger.debug(f"StreamLLMResults.stream_results called with chain: {chain}, input_data: {input_data}")
        try:
            async for partial_result in chain.astream(input_data):
                logger.debug(f"Yielding partial result: {partial_result}")
                yield partial_result
        except Exception as e:
            logger.error(f"Error in StreamLLMResults.stream_results: {str(e)}")
            raise

class StreamManager:
    """
    A class to manage the streaming process.
    
    This class coordinates the streaming of LLM results, handling the queue
    of partial results and the active streaming task.
    """
    def __init__(self):
        """
        Initialize the StreamManager.
        
        Sets up the StreamLLM instance, an asyncio Queue for partial results,
        and a placeholder for the active streaming task.
        """
        self.stream_llm = StreamLLM()
        self.queue = asyncio.Queue()
        self.active_task = None

    async def generate_stream(self, chain, input_data):
        """
        Generate a stream of results from the LLM chain.
        
        This method initializes streaming, processes the input through the chain,
        and puts partial results into the queue.
        
        Args:
            chain: The LLM chain to process the input data.
            input_data: The input data to be processed by the chain.
        """
        await self.stream_llm.init_streaming()
        async for partial_result in self.stream_llm.stream_results(chain, input_data):
            await self.queue.put(partial_result)
        await self.queue.put(None)  # Signal the end of the stream

    async def get_stream(self):
        """
        Retrieve the stream of partial results.
        
        This method yields partial results from the queue until the end of the stream is signaled.
        
        Yields:
            Partial results from the LLM chain.
        """
        while True:
            partial_result = await self.queue.get()
            if partial_result is None:
                break
            yield partial_result

    def start_streaming(self, chain, input_data):
        """
        Start the streaming process.
        
        This method cancels any existing streaming task and creates a new one
        to generate the stream of results.
        
        Args:
            chain: The LLM chain to process the input data.
            input_data: The input data to be processed by the chain.
        """
        if self.active_task:
            self.active_task.cancel()
        self.active_task = asyncio.create_task(self.generate_stream(chain, input_data))
