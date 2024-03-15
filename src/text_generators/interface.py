"""Abstract base class for text generators."""
from pydantic import BaseModel
from typing import List, Dict, Iterator
from src.templates.interface import BaseTemplate
from abc import ABC, abstractmethod


class Generator(BaseModel, ABC):
    """Abstract base class for text generators."""

    template: BaseTemplate
    """The template to use for generating text."""
    
    url: str
    """The URL of the text generation API."""
    
    api_key: str
    """The API key for the text generation API."""
    
    context: List[Dict[str, str]]
    """The context for the text generation request."""
    
    context_window: int
    """The maximum number of tokens to include in the context for the text generation request."""
    
    def set_apikey(self, apikey) -> bool:
        """Set the API key for the text generation API.
        
        Parameters
        ----------
        apikey : str
            The API key for the text generation API.
        
        Returns
        -------
        bool
            `True` if API key was successfully set, `False` otherwise.
        """
        self.api_key = apikey
        return True

    def set_url(self, url) -> bool:
        """Set the URL of the text generation API.
        
        Parameters
        ----------
        url : str
            The URL of the text generation API.
        
        Returns
        -------
        bool
            `True` if URL was successfully set, `False` otherwise.
        """
        self.url = url
        return True
    
    def set_context_window(self) -> bool:
        """Set the maximum number of tokens to include in the context for the text generation request.
        
        Returns
        -------
        bool
            `True` if context window was successfully set, `False` otherwise.
        """
        self.context_window = 16000
        return True
        
    def set_context(self, context) -> List[Dict[str, str]]:
        """Set the context for the text generation request.
        
        Parameters
        ----------
        context : List[Dict[str, str]]
            The context for the text generation request.
        
        Returns
        -------
        List[Dict[str, str]]
            The updated context for the text generation request.
        """
        if not self.context:
            self.context = []
        self.context.append(context)
        return self.context
    
    def set_template(self, template: BaseTemplate) -> List[Dict[str, str]]:
        """Set the template to use for generating text.
        
        Parameters
        ----------
        template : BaseTemplate
            The template to use for generating text.
        
        Returns
        -------
        List[Dict[str, str]]
            The updated context for the text generation request.
        """
        self.template = template
        if self.context[0]["role"] == "system":
            self.context.pop(0)
        self.context.insert(0, self.template.create_system_prompt())
        return self.context        
        
    @abstractmethod
    async def generate(
        self,
        messages: List[Dict[str, str]]
    ) -> Dict[str, str]:
        """Generate a response based on a list of input messages.
        
        Parameters
        ----------
        messages : List[Dict[str, str]]
            The list of input messages.
        
        Returns
        -------
        Dict[str, str]
            The response generated by the text generator.
        """
        pass
    
    @abstractmethod
    async def async_generate(
        self,
        messages: List[Dict[str, str]]
    ) -> Iterator[Dict[str, str]]:
        """
        Asynchronously generate a response based on a list of input messages.
        """
        pass

    @abstractmethod
    def prepare_messages(
        self,
        queries: List[str],
        context: List[Dict[str, str]],
        messages: List[Dict[str, str]]
    ) -> List[Dict[str, str]]:
        """
        Prepares a list of messages for the text generator.
        """
        pass


class GeneratorConfig(BaseModel):
    """
    Configuration for the text generator.
    """
    template: BaseTemplate
    url: str
    api: str
    context: List
    context_window: int
