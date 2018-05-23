# PyDiction
Dictionary App for Windows. Makes use of PyGubu UI designer and Oxford's Dictionary API

1. Fetches JSON content as a response after making request to Oxford's API .
2. Let user choose optional information apart from meaning and usage of the word (tk.Checkbutton)
3. With background as tk.Canvas, rest of the widgets are imposed on the GUI like:
      - tk.Button
      - tk.Entry
      - tk.Label
      - tk.Checkbutton
      - tk.Radiobutton, and also a
      - ttk.Separator
      
4. Play a GIF until the response to the request is received:-

![Screen snapshot when request is made](https://github.com/aseemydv/PyDiction/blob/master/UI/snapshot-search.png)

5. Display the meaning and other optional information inside a tk.Text widget:-

![Screen snapshot after response is received](https://github.com/aseemydv/PyDiction/blob/master/UI/snapshot-result.png)
