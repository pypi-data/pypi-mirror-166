from __future__ import unicode_literals

class DataMigException(BaseException):
    def __init__(self, m):
        self.message = m
    def __str__(self):
        return self.message

class ValidationException(BaseException):
    def __init__(self, m):
        self.message = m
    def __str__(self):
        return self.message

class TranslationException(DataMigException):
    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

    def __str__(self):
        return self.message




class FeatureNotConfiguredError(DataMigException):
    """ Raised when no active configuration found """
    def __init__(self, m):
        self.message = m
    def __str__(self):
        return self.message

class NotInProject(DataMigException):
    """ Raised when no project can be found in the current context """
    def __init__(self, m):
        self.message = m
    def __str__(self):
        return self.message

class ProjectConfigNotFound(DataMigException):
    """ Raised when a project is found in the current context but no configuration was found for the project """
    def __init__(self, m):
        self.message = m
    def __str__(self):
        return self.message


class KeychainNotFound(DataMigException):
    """ Raised when no keychain could be found """
    def __init__(self, m):
        self.message = m
    def __str__(self):
        return self.message


class KeychainKeyNotFound(DataMigException):
    """ Raised when the keychain key couldn't be found """
    def __init__(self, m):
        self.message = m
    def __str__(self):
        return self.message


class OrgNotFound(DataMigException):
    """ Raised when no org could be found by a given name in the project keychain """
    def __init__(self, m):
        self.message = m
    def __str__(self):
        return self.message


class ServiceNotConfigured(DataMigException):
    """ Raised when no service configuration could be found by a given name in the project keychain """
    def __init__(self, m):
        self.message = m
    def __str__(self):
        return self.message


class ServiceNotValid(DataMigException):
    """ Raised when no service configuration could be found by a given name in the project configuration """
    def __init__(self, m):
        self.message = m
    def __str__(self):
        return self.message


class DependencyResolutionError(DataMigException):
    """ Raised when an issue is encountered while resolving a static dependency map """
    def __init__(self, m):
        self.message = m
    def __str__(self):
        return self.message


class ConfigError(DataMigException):
    """ Raised when a configuration enounters an error """
    def __init__(self, m):
        self.message = m
    def __str__(self):
        return self.message



class AntTargetException(DataMigException):
    """ Raised when a generic Ant target error occurs """
    def __init__(self, m):
        self.message = m
    def __str__(self):
        return self.message



class DeploymentException(DataMigException):
    """ Raised when a metadata api deployment error occurs """
    def __init__(self, m):
        self.message = m
    def __str__(self):
        return self.message



class ApexTestException(DataMigException):
    """ Raised when a build fails because of an Apex test failure """
    def __init__(self, m):
        self.message = m
    def __str__(self):
        return self.message



class SalesforceCredentialsException(DataMigException):
    """ Raise when Salesforce credentials are invalid """
    def __init__(self, m):
        self.message = m
    def __str__(self):
        return self.message



class TaskRequiresSalesforceOrg(DataMigException):
    """ Raise when a task that requires a Salesforce org_config is not initialized with an org_config """
    def __init__(self, m):
        self.message = m
    def __str__(self):
        return self.message



class TaskOptionsError(DataMigException):
    """ Raise when a task's options are invalid """
    def __init__(self, m):
        self.message = m
    def __str__(self):
        return self.message



class GithubNotConfigured(DataMigException):
    """ Raise when attempting to get the Github configuration from the keychain and no configuration is set """
    def __init__(self, m):
        self.message = m
    def __str__(self):
        return self.message



class MrbelvedereNotConfigured(DataMigException):
    """ Raise when attempting to get the mrbelvedere configuration from the keychain and no configuration is set """
    def __init__(self, m):
        self.message = m
    def __str__(self):
        return self.message



class ApexTestsDBNotConfigured(DataMigException):
    """ Raise when attempting to get the ApexTestsDB configuration from the keychain and no configuration is set """
    def __init__(self, m):
        self.message = m
    def __str__(self):
        return self.message



class TaskNotFoundError(DataMigException):
    """ Raise when task is not found in project config """
    def __init__(self, m):
        self.message = m
    def __str__(self):
        return self.message


class FlowInfiniteLoopError(DataMigException):
    """ Raised when a flow configuration creates a infinite loop """
    def __init__(self, m):
        self.message = m
    def __str__(self):
        return self.message


class FlowConfigError(DataMigException):
    """ Raised when a flow configuration encounters an error """
    def __init__(self, m):
        self.message = m
    def __str__(self):
        return self.message


class FlowNotFoundError(DataMigException):
    """ Raise when flow is not found in project config """
    def __init__(self, m):
        self.message = m
    def __str__(self):
        return self.message

class FlowNotReadyError(DataMigException):
    """ Raise when flow is called before it has been prepared """
    def __init__(self, m):
        self.message = m
    def __str__(self):
        return self.message



class MrbelvedereError(DataMigException):
    """ Raise for errors from mrbelvedere installer """
    def __init__(self, m):
        self.message = m
    def __str__(self):
        return self.message



class ScratchOrgException(DataMigException):
    """ Raise for errors related to scratch orgs """
    def __init__(self, m):
        self.message = m
    def __str__(self):
        return self.message



class GithubException(DataMigException):
    """ Raise for errors related to GitHub """
    def __init__(self, m):
        self.message = m
    def __str__(self):
        return self.message


class GithubApiError(DataMigException):
    def __init__(self, m):
        self.message = m
    def __str__(self):
        return self.message


class GithubApiNotFoundError(DataMigException):
    def __init__(self, m):
        self.message = m
    def __str__(self):
        return self.message


class GithubApiNoResultsError(DataMigException):
    def __init__(self, m):
        self.message = m
    def __str__(self):
        return self.message


class GithubApiUnauthorized(DataMigException):
    def __init__(self, m):
        self.message = m
    def __str__(self):
        return self.message


class SalesforceException(DataMigException):
    """ Raise for errors related to Salesforce """
    def __init__(self, m):
        self.message = m
    def __str__(self):
        return self.message



class SalesforceDXException(DataMigException):
    """ Raise for errors related to Salesforce DX """
    def __init__(self, m):
        self.message = m
    def __str__(self):
        return self.message



class SOQLQueryException(DataMigException):
    """ Raise for errors related to Salesforce DX """
    def __init__(self, m):
        self.message = m
    def __str__(self):
        return self.message



class CommandException(DataMigException):
    """ Raise for errors coming from spawned CLI subprocesses """
    def __init__(self, m):
        self.message = m
    def __str__(self):
        return self.message



class BrowserTestFailure(CommandException):
    """ Raise when browser tests fail """
    def __init__(self, m):
        self.message = m
    def __str__(self):
        return self.message



class ApexCompilationException(DataMigException):
    """ Raise when apex compilation fails """
    def __init__(self, m):
        self.message = m
    def __str__(self):
        return self.message



class ApexException(DataMigException):
    """ Raise when an Apex Exception is raised in an org """
    def __init__(self, m):
        self.message = m
    def __str__(self):
        return self.message



class PushApiObjectNotFound(DataMigException):
    """ Raise when Salesforce Push API object is not found """
    def __init__(self, m):
        self.message = m
    def __str__(self):
        return self.message


class RobotTestFailure(DataMigException):
    """ Raise when a robot test fails in a test suite """
    def __init__(self, m):
        self.message = m
    def __str__(self):
        return self.message


class SalesforceOAuthError(DataMigException):
    def __init__(self, m):
        self.message = m
    def __str__(self):
        return self.message


class RequestOauthTokenError(DataMigException):

    def __init__(self, message, response):
        super(RequestOauthTokenError, self).__init__(message)
        self.response = response

    def __str__(self):
        return '{}({})'.format(self.message, self.response)

class BatchFailureException(DataMigException):
    def __init__(self, m):
        self.message = m
    def __str__(self):
        return self.message

class RecordErrorException(DataMigException):
    def __init__(self, m):
        self.message = m
    def __str__(self):
        return self.message
