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
          if (withoutTeam){
            if(emp.TeamID == null){
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

}
