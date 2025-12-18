declare namespace NodeJS {
  interface ProcessEnv {
    readonly NODE_ENV: 'development' | 'production' | 'test';
    readonly PUBLIC_URL?: string;
    readonly REACT_APP_API_BASE?: string;
    readonly REACT_APP_FEATURE_X?: string;
    // add additional REACT_APP_ keys here as needed
  }
}
