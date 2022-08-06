import { Component, OnInit } from '@angular/core';
import { AuthService } from 'src/services/auth.service';
import { Chart } from 'chart.js';
import  { TeamService } from 'src/services/team.service';
import { Team } from 'src/models/Team';
import { Employee } from 'src/models/Employee';
import { EmployeeService } from 'src/services/employee.service';
import { catchError } from 'rxjs/operators';

@Component({
  selector: 'app-reports',
  templateUrl: './reports.component.html',
  styleUrls: ['./reports.component.css']
})
export class ReportsComponent implements OnInit {
  teamSearch:any;
  employeeSearch:any;
  myChart: any;
  constructor(private auth: AuthService,private teamService:TeamService,private employeeService:EmployeeService) { }
  teams: Array<any>  = [];
  employees: Array<any> = [];
  ngOnInit(): void {
    //get today date and set it to the input field with id startDate
    let today = new Date();
    let d = Number(today.getDate());
    let mm = Number(today.getMonth() + 1); //January is 0!
    let yyyy = today.getFullYear();
    today = new Date(yyyy, +mm - 1, +d);
    let date = yyyy + '-' + mm + '-' + d;
    let input = document.getElementById('startDate') as HTMLInputElement;
    this.setDate();
    this.getData(d,mm,yyyy);

}
//make event listener for the input field with id startDate and call getData function when the value changes
onDateChange(){
  
  //get the value of the input field
  this.teams = [];
  this.employees = [];
  let input = document.getElementById('startDate') as HTMLInputElement;
  let date = input.value;
  let dd = Number(date.split('-')[2]);
  let mm = Number(date.split('-')[1]);
  let yyyy = Number(date.split('-')[0]);

  this.getData(dd,mm,yyyy);
}
getData(dd:number,mm:number,yyyy:number){
  this.teams = [];
  this.employees = [];
 

  if (this.auth.validateToken() == false) {
    window.location.href = '/login';
  }

  this.employeeService.getAttendReport(yyyy,mm,dd).subscribe(data => {
    this.teams = data['Teams'];
    this.employees = data['Employees'];
    console.log(this.teams);
    console.log(this.employees);
      
    this.myChart?.destroy();
    this.createGraph();
  })

}
setDate(){
        //get today date and set it to the input field with id startDate  with format yyyy-MM-dd 
        let today = new Date();
        let dd = String(today.getDate()).padStart(2, '0');
        let mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
        let yyyy = today.getFullYear();
        today = new Date(yyyy, +mm - 1, +dd);
        let date = yyyy + '-' + mm + '-' + dd;
        let input = document.getElementById('startDate') as HTMLInputElement;
        input.value = date;
}
createGraph(){
  console.log(this.employees)
  let div =  document.getElementById('show') as HTMLDivElement;
  
   //get the canvas element
   var ctx = document.getElementById('chart') as HTMLCanvasElement;
  //sort the teams by the number of attendes

    this.teams.sort((a, b) => (a.Attends > b.Attends) ? -1 : 1)

   ctx.innerHTML = ''
   //get team names as labels
    this.myChart = new Chart(ctx, {
     type: 'bar',
     data: {
         labels: this.teams.map(team => team.TeamName),
         datasets: [{
             label: ' Attendances',
             data: this.teams.map(team => team.Attends),
             backgroundColor: [
                 'rgba(255, 99, 132, 0.2)',
                 'rgba(54, 162, 235, 0.2)',
                 'rgba(255, 206, 86, 0.2)',
                 'rgba(75, 192, 192, 0.2)',
                 'rgba(153, 102, 255, 0.2)',
                 'rgba(255, 159, 64, 0.2)'
             ],
             borderColor: [
                 'rgba(255, 99, 132, 1)',
                 'rgba(54, 162, 235, 1)',
                 'rgba(255, 206, 86, 1)',
                 'rgba(75, 192, 192, 1)',
                 'rgba(153, 102, 255, 1)',
                 'rgba(255, 159, 64, 1)'
             ],
             borderWidth: 1
         }]
     },
     options: {

         scales: {
             y: {
                 beginAtZero: true,
             },

         }
     },
     //sort the data by the number of attendes
     
 });
  div.style.display = 'block';

}

}