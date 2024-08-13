class IndexerError(Exception):
    """Base exception class for the indexer project."""
    pass

class ConfigurationError(IndexerError):
    """Exception raised for configuration-related errors."""
    pass

class URLValidationError(IndexerError):
    """Exception raised for URL validation errors."""
    pass