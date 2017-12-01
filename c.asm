section .data
       a dd 1
       e dq 1.2,2.3,4.5
       f dq 3.4
       string db "this is a string"
       n dd 17
       b dd 12
section .bss 
       c resb 2
       d resd 5
       s resb 17 
section .text
       global main
       extern printf
main:
       mov ebx,12
       mov ebx,ebx
       mov ebx,dword[a]
       mov dword[ebx],12
       mov dword[eax],12
       mov dword[a],66
       mov dword[a],ebx
       mov ebx,dword[b]
       mov dword[b],ebx
       mov dword[ecx],ebx
       mov eax,dword[ebx]   

       add eax,ebx
       add ecx,ebx
       add ebx,dword[a]
       add dword[a],ebx
       add ebx,13
       add dword[a],4
       add dword[eax],77 
       add dword[ebx],12 
           
       add dword[eax],ebx 
       add ebx,dword[eax]
      
       sub eax,ebx
       sub ecx,ebx
       sub ebx,dword[a]
       sub dword[a],ebx
       sub ebx,12
       sub ecx,12
       sub dword[a],12
       sub dword[eax],12 
       sub dword[ebx],12 
           
       sub dword[eax],ebx 
       sub ebx,dword[eax]
       mov eax,0
       mov ecx,dword[n]
       mov esi,string
       mov edi,s 
       movsb
       lodsb
       cld
       std
       mov al,"s"
       mov ecx,17 
       mov edi,string
       rep scasb
           

        
 


