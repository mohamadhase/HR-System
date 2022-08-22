import { Injectable } from '@angular/core';
import { Team } from 'src/models/Team';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { AppSettings } from './AppSettings';
import { Employee } from 'src/models/Employee';
import { catchError, Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class TeamService {
  token: string = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJVc2VyTmFtZSI6InN0cmluZyIsImV4cCI6MTY1OTcwMjI1Nn0.P_4czf5UuT4Z_8fZFaNHSQNB1FiU2Wc1RX92-Suzojw'
  constructor(private http: HttpClient) { }
  //create function to get all teams
  getTeams(): Array<Team> {
    let teams = new Array<Team>();

    this.http.get(`${AppSettings.API_ENDPOINT}organization/info?employees=0&teams=1`, { headers: AppSettings.HEADER })
      .subscribe(data => {
        for (let team of Object(data)['Teams']) {
          let obj: Team = {
            Name: team['Name'],
            Description: team['Description']
          }
          teams.push(obj);
        }
      })
    return teams;
  }
  getTeamsObservable(): Observable<any> {
    return this.http.get(`${AppSettings.API_ENDPOINT}organization/info?employees=0&teams=1`, { headers: AppSettings.HEADER })
  }
  deleteTeam(teamid: string): void {

    this.http.delete(`${AppSettings.API_ENDPOINT}}/team/${teamid}`, { headers: AppSettings.HEADER }).subscribe()
  }
  updateTeam(team: Team, description: string): void {

    this.http.patch(`${AppSettings.API_ENDPOINT}/team/${team.Name}?Description=${description}`, NaN, { headers: AppSettings.HEADER }).subscribe()
  }
  getTeamEmployees(teamid: string): Array<Employee> {
    let employees = new Array<Employee>();

    this.http.get(`${AppSettings.API_ENDPOINT}team/${teamid}/employees`, { headers: AppSettings.HEADER }).subscribe(data => {
      for (let employee of Object(data)) {
        let obj: Employee = {
          ID: employee['ID'],
          Name: employee['Name'],
          Email: employee['Email'],
          Phone: employee['Phone'],
          TeamID: employee['TeamID'],
          SlackID: employee['SlackID'],
          HourPrice: employee['HourPrice'],
          Address: employee['Address']
        }

        employees.push(obj);

      }

    })
    return employees;
  }
  getTeamEmployeesObservable(teamid: string): Observable<any> {
    return this.http.get(`${AppSettings.API_ENDPOINT}team/${teamid}/employees`, { headers: AppSettings.HEADER })
  }
  removeEmployeeFromTeam(employeeid: string, teamid: string): void {
    this.http.delete(`${AppSettings.API_ENDPOINT}team/${teamid}/employees?employee_id=${employeeid}`, { headers: AppSettings.HEADER }).subscribe()
  }

  newTeam(team: Team): Observable<any> {
    let code = 200;
    return this.http.post(`${AppSettings.API_ENDPOINT}team/`, team, { headers: AppSettings.HEADER })
  }
  addEmployeeToTeam(employeeid: string, teamid: string): void {
    this.http.post(`${AppSettings.API_ENDPOINT}team/${teamid}/employees?employee_id=${employeeid}`, NaN, { headers: AppSettings.HEADER }).subscribe()
  }
}