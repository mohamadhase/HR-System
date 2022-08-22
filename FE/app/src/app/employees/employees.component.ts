import { Component, OnInit } from '@angular/core';
import { catchError } from 'rxjs/operators';
import { Employee } from 'src/models/Employee';
import { EmployeeService } from 'src/services/employee.service';
import { AuthService } from 'src/services/auth.service';
@Component({
  selector: 'app-employees',
  templateUrl: './employees.component.html',
  styleUrls: ['./employees.component.css']
})
export class EmployeesComponent implements OnInit {
  employees:Array<Employee> = [];
  employeeSlack:any;
  searchText:any;

  constructor(private employeeService:EmployeeService,private auth:AuthService) { }
  ngOnInit(): void {
    if (this.auth.validateToken()==false){
      window.location.href = "/home";
    }
    this.employees = this.employeeService.getAllEmployees();

  }
  deleteEmployee(id:string){
    if (confirm("Are you sure?")){
      this.employeeService.deleteEmployee(id);
      this.employees.splice(this.employees.findIndex(x => x.ID == id),1);
    }

  }

  updateEmployee(id:string){
    //get inputs values 
    let name = (<HTMLInputElement>document.getElementById("empName"))?.value;
    let email = (<HTMLInputElement>document.getElementById("empEmail"))?.value;
    let phone = (<HTMLInputElement>document.getElementById("empPhone"))?.value;
    let address = (<HTMLInputElement>document.getElementById("empAddress"))?.value;
    if (name == "" || email == "" || phone == "" || address == ""){
      alert("All fields are required");
      return;
    }
    let employee:Employee = {
      ID:id,
      Name:name,
      Email:email,
      Phone:phone,
      Address:address,
      TeamID:'',
      SlackID:'',
      HourPrice:''
    }
    this.employeeService.updateEmployee(employee);
    this.employees[this.employees.findIndex(x => x.ID == id)] = employee;
    alert("Employee updated successfully");
  }

  createEmployee(){
    //get inputs values 
    let ID = (<HTMLInputElement>document.getElementById("newID"))?.value;
    let Name = (<HTMLInputElement>document.getElementById("newName"))?.value;
    let Email = (<HTMLInputElement>document.getElementById("newEmail"))?.value;
    let Phone = (<HTMLInputElement>document.getElementById("newPhone"))?.value;
    let Adreess = (<HTMLInputElement>document.getElementById("newAddress"))?.value;
    let Slack = (<HTMLInputElement>document.getElementById("newSlack"))?.value;
    let Hour = (<HTMLInputElement>document.getElementById("newHour"))?.value;
    let Error = document.getElementById('Error') as HTMLParagraphElement;

    
    if (ID == "" || Name == "" || Email == "" || Phone == "" || Adreess == "" || Slack == "" || Hour == ""){
      alert("All fields are required");
      return;
    }
    
    
 
    let employee:Employee = {
      ID:ID,
      Name:Name,
      Email:Email,
      Phone:Phone,
      Address:Adreess,
      TeamID:'',
      SlackID:Slack,
      HourPrice:Hour
    }
    this.employeeService.createEmployee(employee).pipe(
      catchError(error => {
        Error.innerHTML = `the team ${employee.ID} already exists`;
        Error.style.color = 'red';
        return ([]);
      })
    ).subscribe(
      data => {
        this.employees.push(employee);
        Error.innerHTML = `Employee ${employee.ID} created`;
        Error.style.color = 'green';
      }
    )
  }
  getSlackInfo(id:string){
    let img = document.getElementById('slackimg') as HTMLImageElement;
    this.employeeService.getSlackInfo(id).subscribe(data=>{
      if (data['ok']==false){
       alert('Slack user not found');
       //redirect the user to the home page
       console.log(data);
      }
      console.log(data['user']);
      this.employeeSlack = data['user'];

     })
  }

}
