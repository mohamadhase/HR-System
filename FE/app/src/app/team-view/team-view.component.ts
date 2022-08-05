import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Employee } from 'src/models/Employee';
import { TeamService } from '../../services/team.service';
import { EmployeeService } from 'src/services/employee.service';
@Component({
  selector: 'app-team-view',
  templateUrl: './team-view.component.html',
  styleUrls: ['./team-view.component.css']
})
export class TeamViewComponent implements OnInit {
  teamName:string = "";
  employees :Array<Employee>=[];
  noTeamEmployees: Array<Employee> = [];
  constructor(private route:ActivatedRoute,private teamService:TeamService,private employeeService:EmployeeService) { }

  ngOnInit(): void {
    this.route.params.subscribe(params=>{
      this.teamName = params['id'];
    }

    )
   this.employees = this.teamService.getTeamEmployees(this.teamName);
   
  }
  deleteEmployee(employee:Employee){
    if(confirm("Are you sure to delete "+employee.Name+"?")) {
      this.teamService.removeEmployeeFromTeam(employee.ID,this.teamName);
      this.employees.splice(this.employees.indexOf(employee),1);
    }
  }
  getNoTeamEmployees(){
    //get the employees who are have TeamID = None
    this.noTeamEmployees = this.employeeService.getAllEmployees(true)
  }
  addEmployeeToTeam(){
    //get selector with id employeeSelector
    let employeeID = (<HTMLSelectElement>document.getElementById("employeeSelector")).value;
    if (employeeID != ""){
      this.teamService.addEmployeeToTeam(employeeID,this.teamName);
      this.employees.push(this.employeeService.getEmployee(employeeID));
      alert("Employee added to team");
      window.location.href = "/team/"+this.teamName;

      
    }
    else{
      alert("Please select an employee");
    }
  }
}
