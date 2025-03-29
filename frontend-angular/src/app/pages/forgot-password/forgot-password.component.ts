import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-forgot-password',
  templateUrl: './forgot-password.component.html',
  styleUrls: ['./forgot-password.component.css'],
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterModule]
})
export class ForgotPasswordComponent {
  forgotPasswordForm: FormGroup;
  loading = false;
  error = '';
  success = false;

  constructor(
    private formBuilder: FormBuilder,
    private authService: AuthService,
    private router: Router
  ) {
    this.forgotPasswordForm = this.formBuilder.group({
      email: ['', [Validators.required, Validators.email]]
    });
  }

  onSubmit(): void {
    if (this.forgotPasswordForm.invalid) {
      Object.keys(this.forgotPasswordForm.controls).forEach(key => {
        const control = this.forgotPasswordForm.get(key);
        if (control?.invalid) {
          control.markAsTouched();
        }
      });
      return;
    }

    this.loading = true;
    this.error = '';
    this.success = false;

    const { email } = this.forgotPasswordForm.value;

    this.authService.forgotPassword(email).subscribe({
      next: (response) => {
        console.log('Resposta da API:', response);
        this.success = true;
        this.loading = false;
      },
      error: (err) => {
        console.error('Erro da API:', err);
        this.loading = false;
        if (err.status === 404) {
          this.error = 'Email não encontrado';
        } else {
          this.error = 'Erro ao processar a solicitação. Tente novamente mais tarde.';
        }
      }
    });
  }
} 