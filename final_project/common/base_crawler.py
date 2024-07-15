from abc import ABC, abstractmethod


class BaseCrawler(ABC):
    @abstractmethod
    def crawl_data(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def save_data(self, raw_data, file):
        raise NotImplementedError

    @abstractmethod
    def executor(self):
        raise NotImplementedError
