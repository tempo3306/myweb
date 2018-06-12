import axios from 'axios'

const instance = axios.create({
    baseURL: '',
    timeout: 3 * 1000,
    headers: {'Content-Type': 'application/x-www.form-urlencoded;'}
});

export default instance;
