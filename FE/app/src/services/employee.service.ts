import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Employee } from 'src/models/Employee';
import { AppSettings } from './AppSettings';
@Injectable({
  providedIn: 'root'
})
export class EmployeeService {

  constructor(private http:HttpClient) { }
  getAllEmployees(withoutTeam=false):Array<Employee>{
    let employee:Array<Employee> = [];
    this.http.get<Array<Employee>>(AppSettings.API_ENDPOINT + 'organization/info?employees=1&teams=0',{headers:AppSettings.HEADER}).subscribe(
      data => {
        for(let emp of Object(data)['Employees']){
          if (withoutTeam==true){
            if(emp.TeamID == null||emp.TeamID == ''){
              let obj:Employee = {
            ID:emp['ID'],
            Name:emp['Name'],
            Email:emp['Email'],
            Phone:emp['Phone'],
            TeamID:emp['TeamID'],
            SlackID:emp['SlackID'],
            HourPrice:emp['HourPrice'],
            Address:emp['Address']
          }
          employee.push(obj);
            }
          }
          else{
          let obj:Employee = {
            ID:emp['ID'],
            Name:emp['Name'],
            Email:emp['Email'],
            Phone:emp['Phone'],
            TeamID:emp['TeamID'],
            SlackID:emp['SlackID'],
            HourPrice:emp['HourPrice'],
            Address:emp['Address']
          }
          employee.push(obj);
        }
        }
      }
    );
    return employee;
  }
  getEmployee(id:string):Employee{
    let employee:Employee = {} as Employee;
    this.http.get<Employee>(AppSettings.API_ENDPOINT + 'employee/' + id,{headers:AppSettings.HEADER}).subscribe(
      data => {
        employee = {
          ID:data['ID'],
          Name:data['Name'],
          Email:data['Email'],
          Phone:data['Phone'],
          TeamID:data['TeamID'],
          SlackID:data['SlackID'],
          HourPrice:data['HourPrice'],
          Address:data['Address']
        }
        
      }
    )
    return employee;
  }
  deleteEmployee(id:string):void{
     this.http.delete(AppSettings.API_ENDPOINT + 'employee/' + id,{headers:AppSettings.HEADER}).subscribe();
  }
  updateEmployee(employee:Employee):void{
    this.http.put(AppSettings.API_ENDPOINT + 'employee/' +
     employee.ID+`?employee_address=${employee.Address}&employee_phone=${employee.Phone}&employee_email=$${employee.Email}&employee_name=${employee.Name}`,NaN,{headers:AppSettings.HEADER}).subscribe();
  }

  createEmployee(employee:Employee): Observable<any>{
    return this.http.post(AppSettings.API_ENDPOINT + 'employee/',employee,{headers:AppSettings.HEADER});
  }
  getSlackInfo(id:string):Observable<any>{
    let body = new URLSearchParams();
    body.set('token',AppSettings.SLACK_TOKEN);
    return this.http.post(AppSettings.SLACK_END_POINT + 'users.info?user='+id,body,{headers:AppSettings.SLACK_HEADER});
  }
  //http://localhost:5000/employee/111/attendance?Year=11&Month=10&Day=2011
  getEmployeeAttendance(id:string,year:number,month:number,day:number):Observable<any>{
    return this.http.get(AppSettings.API_ENDPOINT + 'employee/' + id + '/attendance?Year=' + year + '&Month=' + month + '&Day=' + day,{headers:AppSettings.HEADER});
  }
  getAttendReport(year:number,month:number,day:number):Observable<any>{
    return this.http.get(AppSettings.API_ENDPOINT + 'employee' + '/get_all_attend?Year=' + year + '&Month=' + month + '&Day=' + day,{headers:AppSettings.HEADER});
  }

}
