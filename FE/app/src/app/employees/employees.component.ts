import { Component, OnInit } from '@angular/core';
import { Employee } from 'src/models/Employee';
import { EmployeeService } from 'src/services/employee.service';

@Component({
  selector: 'app-employees',
  templateUrl: './employees.component.html',
  styleUrls: ['./employees.component.css']
})
export class EmployeesComponent implements OnInit {
  employees:Array<Employee> = [];
  constructor(private employeeService:EmployeeService) { }

  ngOnInit(): void {
    this.employees = this.employeeService.getAllEmployees();

  }

}
