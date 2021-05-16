export type ApiRequest = {
  url: string;
  method: string;
  body?: {};
}

/**
 * API Request handler.
 * 
 * @param url - api endpoint
 * @param method - http method
 * @param body - body parameters of request
 */
const apiRequest =  (req: ApiRequest): Promise<any> => {
  return fetch(req.url, {
    method: req.method,
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: req.body ? JSON.stringify(req.body) : undefined
  })
  .then(resp => {
    if(resp.status != 200) {
      throw new Error(resp.status.toString());
    }
    return resp.json();
  })
  .catch(function(error) {
    throw error;
  });
}

export default apiRequest;
