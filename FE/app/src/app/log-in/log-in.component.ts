import { Component, OnInit } from '@angular/core';
import { catchError } from 'rxjs/operators';
import { AuthService } from 'src/services/auth.service';

@Component({
  selector: 'app-log-in',
  templateUrl: './log-in.component.html',
  styleUrls: ['./log-in.component.css']
})
export class LogInComponent implements OnInit {

  constructor(private auth:AuthService) { }

  ngOnInit(): void {
    if (this.auth.validateToken()==true){
      window.location.href = "/home";
    }

  }
  login(){
    //get inputs values
    let username = (<HTMLInputElement>document.getElementById("username")).value;
    let password = (<HTMLInputElement>document.getElementById("password")).value;
    if (username == "" || password == ""){
      alert("All fields are required");
      return;
    }
    this.auth.login(username,password).pipe(catchError(err => {
      alert('UserName or Password is incorrect');
      return [];
    }
    )).subscribe(res => {
      // localStorage.setItem('token', res);  
      localStorage.setItem('token', String(res));
      localStorage.getItem('token');
      window.location.href = "/home";
    }
    )
  }

}
