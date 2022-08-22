import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { AppSettings } from './AppSettings';
import jwt_decode from 'jwt-decode';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  constructor(private http:HttpClient) { }
  login(email:string,password:string){
    let body = {
      "UserName": email,
      "Password": password
    }
     return this.http.post(AppSettings.API_ENDPOINT + 'authentication/login',body,{headers:AppSettings.HEADER});
      
    
  }
  getDecodedAccessToken(token: string): any {
    try {
      return jwt_decode(token);
    } catch(Error) {
      return null;
    }
  }
  validateToken(){
    let token = localStorage.getItem('token');
    if (token == null){
      return false;
    }
    let decoded = this.getDecodedAccessToken(token);
    if (decoded == null){
      return false;
    }
    if (decoded.exp < Date.now() / 1000){
      return false;
    }
    return true;
  }
  logOut(){
    localStorage.removeItem('token');
  }

}
