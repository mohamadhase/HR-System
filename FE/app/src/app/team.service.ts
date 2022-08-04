import { Injectable } from '@angular/core';
import { Team } from 'src/models/Team';
import { HttpClient,HttpHeaders } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class TeamService {

  constructor(private http:HttpClient) { }
  //create function to get all teams
  getTeams():void {
    var headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'x-acess-token': `eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJVc2VyTmFtZSI6InN0cmluZyIsImV4cCI6MTY1OTYxNjcxM30.CxDKprt46wBq6bwzwraU2UYL_iNOAggo4SczuPL0Xgk`
    })
    this.http.get('http://localhost:5000/organization/info?employees=0&teams=0',{ headers: headers })
    .subscribe(data => {
      console.log(data);
    })
    
  }
}
