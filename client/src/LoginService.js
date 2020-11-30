/* eslint-disable */ 
import axios from 'axios';

const url = 'http://localhost:5000/login';


class LoginService{

    static SendLogin(userName,password){
        return new Promise(async (resolve, reject) =>{
            try{
                const res = await axios.post(url,{},
                    {
                      auth: {
                        username: this.userName,
                        password: this.password,
                      },
                    }
                  )
                const data = res.data;
                resolve(
                    data.map(token =>({
                        ...token,
                    }))
                );
            }
            catch(err){
                reject(err);
            }
        })
    }

}

export default LoginService