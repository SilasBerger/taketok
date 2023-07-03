use crate::config::Config;
use crate::core_api_client::CoreApiClient;

pub struct TakeTokState {
    pub core_api_client: CoreApiClient,
    pub config: Config,
}