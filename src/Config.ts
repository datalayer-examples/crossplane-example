let config = {
    exampleServer: '',
};

export const setConfig = (c: any) => {
    config = c;
}

export const getConfig = () => {
    return config;
}
