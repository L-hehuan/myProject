const baseUrl = 'http://172.20.10.6:4444';  
const nowTime = Date.now || function () {  
    return new Date().getTime();  
};  
export default {  
    baseUrl,  
    nowTime,  
}  