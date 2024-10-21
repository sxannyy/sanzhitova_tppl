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
        mov [result], al
        print result, 1
        dec rbx
        cmp rbx, 0
        jg %%digit
    popd
%endmacro

section .text
global _start

_start:
    mov rax, 0
    mov rbx, 0
    
    jmp check_lens
    
check_lens:
    mov eax, x_len
    mov ebx, y_len
    cmp eax, ebx
    jne _end
    
    mov rax, 0
    mov rbx, 0
    jmp calculate_differences

calculate_differences:
    add eax, [x + 4*rbx]
    sub eax, [y + 4*rbx]
    
    inc rbx
    cmp rbx, x_len
    jne calculate_differences
    
    jmp print_minus_sign

print_minus_sign:
    cmp eax, 0
    jnl print_mean
    print minus, mlen
    neg eax

print_mean:
    mov rcx, x_len
    div rcx
    dprint
    cmp rdx, 0
    je print_done
    jmp print_point
    
print_point:
    print point, plen
    mov rbx, 0
    jmp print_f
    
print_f:
    mov rcx, 10
    mov rax, rdx
    mul rcx
    mov rcx, x_len
    div rcx
    dprint
    inc rbx
    cmp rdx, 0
    je print_done
    cmp rbx, 10
    jle print_f
    
print_done:
    print newline, nlen
    print done_mess, len_mess
    jmp _end

_end:
    mov rax, 60
    xor rdi, rdi
    syscall

section .data
    x dd 5, 3, 2, 6, 1, 7, 4
    x_len equ (($ - x) / 4)
    y dd 0, 10, 1, 9, 2, 8, 5
    y_len equ (($ - y) / 4)

    newline db 0xA, 0xD
    nlen equ $ - newline
    
    minus db '-'
    mlen equ $ - minus
    
    point db '.'
    plen equ $ - point

    done_mess db 'Done', 0xA, 0xD
    len_mess equ $ - done_mess
    
section .bss
    result resb 16
