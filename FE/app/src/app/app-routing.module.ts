import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { EmployeesComponent } from './employees/employees.component';
import { HomeComponent } from './home/home.component';
import { LogInComponent } from './log-in/log-in.component';
import { RegisterComponent } from './register/register.component';
import { ReportsComponent } from './reports/reports.component';
import { TeamViewComponent } from './team-view/team-view.component';
import { TeamsComponent } from './teams/teams.component';

const routes: Routes = [{ path: '', redirectTo: 'home', pathMatch: 'full' }, 
{ path: 'home', component: HomeComponent },
{path:'login',component:LogInComponent},
{path :'register',component:RegisterComponent},
{path:'employees',component:EmployeesComponent},
{path:'teams',component:TeamsComponent},
{path:'team/:id',component:TeamViewComponent},
{path:'employees',component:EmployeesComponent},
{path:'reports',component:ReportsComponent}
];



@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
