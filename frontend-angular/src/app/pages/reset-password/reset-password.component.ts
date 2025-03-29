import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { Router, RouterModule, ActivatedRoute } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-reset-password',
  templateUrl: './reset-password.component.html',
  styleUrls: ['./reset-password.component.css'],
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterModule]
})
export class ResetPasswordComponent implements OnInit {
  resetPasswordForm: FormGroup;
  loading = false;
  error = '';
  success = false;
  token: string | null = null;
  tokenValid = false;

  constructor(
    private formBuilder: FormBuilder,
    private authService: AuthService,
    private router: Router,
    private route: ActivatedRoute
  ) {
    this.resetPasswordForm = this.formBuilder.group({
      new_password: ['', [Validators.required, Validators.minLength(6)]],
      confirm_password: ['', [Validators.required]]
    }, { validator: this.passwordMatchValidator });
  }

  ngOnInit() {
    this.token = this.route.snapshot.queryParamMap.get('token');
    if (!this.token) {
      this.error = 'Token não fornecido';
      this.router.navigate(['/login']);
      return;
    }

    // Verifica se o token é válido
    this.authService.verifyResetToken(this.token).subscribe({
      next: () => {
        this.tokenValid = true;
      },
      error: (err) => {
        this.error = 'Token inválido ou expirado';
        this.router.navigate(['/login']);
      }
    });
  }

  passwordMatchValidator(g: FormGroup) {
    return g.get('new_password')?.value === g.get('confirm_password')?.value
      ? null
      : { mismatch: true };
  }

  onSubmit(): void {
    if (this.resetPasswordForm.invalid) {
      Object.keys(this.resetPasswordForm.controls).forEach(key => {
        const control = this.resetPasswordForm.get(key);
        if (control?.invalid) {
          control.markAsTouched();
        }
      });
      return;
    }

    if (!this.token || !this.tokenValid) {
      this.error = 'Token inválido';
      return;
    }

    this.loading = true;
    this.error = '';
    this.success = false;

    const { new_password } = this.resetPasswordForm.value;

    this.authService.resetPassword(this.token, new_password).subscribe({
      next: () => {
        this.success = true;
        this.loading = false;
        // Redireciona para o login após 3 segundos
        setTimeout(() => {
          this.router.navigate(['/login']);
        }, 3000);
      },
      error: (err) => {
        this.loading = false;
        if (err.status === 400) {
          this.error = 'Token inválido ou expirado';
          this.router.navigate(['/login']);
        } else {
          this.error = 'Erro ao redefinir senha. Tente novamente mais tarde.';
        }
      }
    });
  }
} 