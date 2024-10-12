%macro pushd 0
   push rax
   push rbx
   push rcx
   push rdx
%endmacro

%macro popd 0
   pop rdx
   pop rcx
   pop rbx
   pop rax
%endmacro

%macro print 2
   pushd
   mov rax, 1
   mov rdi, 1
   mov rsi, %1
   mov rdx, %2
   syscall
   popd
%endmacro

%macro dprint 0
   pushd
   mov rbx, 0
   mov rcx, 10
   %%divide:
       xor rdx, rdx
       div rcx
       push rdx
       inc rbx
       cmp rax, 0
       jne %%divide

   %%digit:
       pop rax
       add rax, '0'
       mov [char_buf], al
       print char_buf, 1
       dec rbx
       cmp rbx, 0
       jg %%digit
   popd
%endmacro

section .text
global _start

_start:
start_guess:
   mov eax, dword [value]
   mov dword [g_num], eax
   mov dword [g_den], dword 2
   
calc_next:
   xor rax, rax
   mov eax, dword [value]
   mul dword [g_den]
   mul dword [g_den]
   mov dword [n_num], eax
   mov eax, dword [g_num]
   mul dword [g_num]
   add dword [n_num], eax
   mov eax, dword [g_num]
   mul dword [g_den]
   mov ecx, 2
   mul ecx
   mov dword [n_den], eax
   mov eax, dword [n_num]
   div dword [n_den]
   mov dword [n_num], eax
   mov dword [n_den], dword 1
   
check_diff:
   mov eax, dword [n_num]
   mul dword [g_den]
   mov edx, eax
   mov eax, dword [g_num]
   sub eax, edx
   cmp eax, dword [g_den]
   jl done
   
update_guess:
   mov edx, dword [n_num]
   mov [g_num], edx
   mov edx, dword [n_den]
   mov [g_den], edx
   jmp calc_next
   
done:
   mov eax, dword [n_num]
   dprint
   print newline, nlen
   print finished, flen
   mov rax, 60
   xor rdi, rdi
   syscall

section .data
   value dd 169

   newline db 0xA, 0xD
   nlen equ $ - newline
   
   finished db 'Done', 0xA, 0xD
   flen equ $ - finished

section .bss
   char_buf resb 16
   g_num resd 1
   g_den resd 1
   n_num resd 1
   n_den resd 1

