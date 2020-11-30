/* eslint-disable */ 
import axios from 'axios';

const url = 'http://localhost:5000/account/';


class UserService{

    static getUser(){
        return new Promise(async (resolve, reject) =>{
            try{
                const res = await axios.get(url, {
                    headers: {
                      'x-access-token': document.cookie
                  
                    }
                   
                  }); console.log('sent')
                const data = res.data;
                console.log(data);
                resolve(
                    data.map(user =>({
                        ...user,
                    }))
                );
            }
            catch(err){
                reject(err);
            }
        })
    }

    static insertPost(text){
        return axios.post(url,{
            text
        });
    }
    static deletePost(id){
        return axios.delete('${url}${id}');
    }
}

export default UserService