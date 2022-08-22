import { Component, OnInit } from '@angular/core';
import { AuthService } from 'src/services/auth.service';
@Component({
  selector: 'app-nav',
  templateUrl: './nav.component.html',
  styleUrls: ['./nav.component.css']
})
export class NavComponent implements OnInit {
  logined = false;
  username :string = "";
  constructor(private auth:AuthService) { }
  ngOnInit(): void {
    if (this.auth.validateToken()==true){
      this.logined = true;
      this.username = this.auth.getDecodedAccessToken(String(localStorage.getItem('token'))).UserName;
    }
  }
  logOut(){
    this.auth.logOut();
    window.location.href = "/home";
  }

}
