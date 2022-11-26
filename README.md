Re-organize the project's file system (adopted to dir that link to Docker container)

https://lucid.app/lucidchart/2557aaa7-1d14-4c47-a025-b83c4d611562/edit?viewport_loc=157%2C76%2C1220%2C821%2C0_0&invitationId=inv_8edfb715-fb5f-418d-977d-312b47235688

- Implementation mainly contains .py code (source code)
- data folder contains NVD SARD source data and its derivations.


- co kha nang slice cua sard or nvd will overwrite the other one; 3 file khac ten nen ko dc doc
=> set their output to the same files and change mode to 'a' - append