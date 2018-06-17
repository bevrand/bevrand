const sanitizeUrl = (url) => {
  let newUrl;
  newUrl = url.startsWith('http://') ? url : 'http://' + url;
  newUrl = url.endsWith('/') ? url.substring(0, url.length - 1) : url;
  return newUrl;
}


const Config = {
  proxyHostname: sanitizeUrl(process.env.REACT_APP_PROXY_HOSTNAME || 'http://localhost:4540'),
}

export default Config;