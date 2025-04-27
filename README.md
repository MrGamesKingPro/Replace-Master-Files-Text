# Replace-Master-Files-Text
- This application allows you to search for multiple blocks of text (each potentially spanning multiple lines) and replace them with corresponding blocks of text.
- It can operate on a single text file, multiple text files simultaneously, or even text pasted directly into the application.

[Download Replace Master Files Text](https://github.com/MrGamesKingPro/Replace-Master-Files-Text/releases/tag/Replace.Master.Files.Text)

Or use a version Python

Install Libraries

pip install ttkbootstrap

![Sans titre 2](https://github.com/user-attachments/assets/18feef6c-d6c3-4bdb-9549-8c00aa207595)


Menu Bar (Top):

    - File: Open File(s), Save, Save Preview As, Exit.

    - Edit: Copy, Cut, Paste, Select All, Clear All / Reset.

    - Language: Switch between English and Arabic.

    - Help: Show the About dialog.

Input Section (Upper Area):

    - Search For (one per line): A text box where you enter the text strings you want to find. Each distinct search term should be on its own line.

    - Replace With (corresponding line): A text box where you enter the replacement text. The text on line N here will replace the text found from line N in the "Search For" box. The number of lines in both boxes must match.

Action Buttons (Middle Area):

    - Preview Replacements: Performs the search based on the input boxes and shows the potential result in the "After" pane without modifying any files yet.

    - Clean Input Fields: Removes leading/trailing whitespace from each line in the "Search For" and "Replace With" boxes (useful for tidying up).

Preview Section (Lower Area - Resizable):

    - Before (Original Content): Displays the original content of the loaded file(s) or pasted text. If multiple files are loaded, they are shown sequentially with separators like --- File: filename.txt ---. This pane is read-only after loading files but editable if you paste text directly.

    - After (Preview): Displays the content after the replacements have been previewed using the "Preview Replacements" button. This pane is always read-only.

    - Search Bars: Below both the "Before" and "After" panes, there's a small search bar (Search: [Entry] Find Next) to help you find specific text within that pane (this doesn't perform the main replacement).

 Basic Workflow (Single or Multiple Files):

    Load Content:

        - Option A (Load Files): Go to File -> Open File(s)... (or press Ctrl+O). Select one or more text files. Their content will appear concatenated in the "Before" pane (with separators if multiple). The "Before" pane becomes read-only.

        - Option B (Paste Text): If you don't load files, you can copy text from elsewhere and paste it directly into the "Before" pane (using Ctrl+V or Edit -> Paste or Right-Click -> Paste). In this case, the "Before" pane remains editable.

    Enter Search Terms: In the "Search For" box, type or paste the text you want to find. Put each distinct search term on a new line.

    Enter Replace Terms: In the "Replace With" box, type or paste the corresponding replacement text. Ensure the line number here matches the line number of the search term it should replace. You must have the same number of lines in both boxes.

    (Optional) Clean Inputs: Click "Clean Input Fields" to remove extra whitespace from the search/replace terms.

    Preview: Click the Preview Replacements button. The application will process the text from the "Before" pane using your search/replace rules. The result will appear in the "After" pane. The status bar will indicate how many replacements were made in the preview.

    Review: Check the "After" pane carefully to ensure the replacements are correct. You can use the small search bar below the "After" pane to find specific parts of the result.

    Save Changes (Choose Carefully!):

        - To Overwrite Original Files (Save): If you loaded file(s) and are happy with the preview, go to File -> Save (or press Ctrl+S). This will apply the search/replace rules again to the original content of each loaded file individually and overwrite those original files. This is permanent! Use with caution. The * in the title bar will disappear. (This option does nothing if you only pasted text into "Before").

        - To Save Preview to a New File (Save Preview As): If you want to save the exact content shown in the "After" preview pane to a new file (leaving originals untouched, or saving pasted/modified content), go to File -> Save Preview As... (or press Ctrl+Shift+S). You'll be prompted for a new filename. This is safer and also works if you pasted text initially. After saving, the application resets, treating the newly saved file as the content in the "Before" pane.

 Other Actions:

    Clear All / Reset: Use Edit -> Clear All / Reset to clear all text boxes, remove loaded file information, and reset the application to its initial state. It will warn you if you have unsaved changes.

    Language Switching: Use the Language menu to change the interface language between English and Arabic (includes Right-to-Left layout adjustments for Arabic).

    Standard Editing: Use the Edit menu, keyboard shortcuts (Ctrl+C, Ctrl+X, Ctrl+V, Ctrl+A), or the right-click context menu in the text boxes for standard copy, cut, paste, and select all operations. (Cut/Paste are only enabled in editable fields: Search, Replace, and Before only if no file is loaded).

    Find in Panes: Use the Search: entry and Find Next button below the "Before" or "After" panes to quickly locate text within that specific display area. Pressing Enter in the search entry also triggers "Find Next". Found text is highlighted temporarily.

    Unsaved Changes: If the "After" preview differs from the original "Before" content, an asterisk (*) appears in the title bar. The app will prompt you to save or discard these changes if you try to open new files, clear all, or exit.

 Important Notes:

    Save vs. Save Preview As: Understand the difference! Save overwrites originals; Save Preview As creates a new file from the preview.

    Line Count Match: The number of lines in "Search For" must equal the number of lines in "Replace With".

    Text Files Only: The application treats all files as text. Opening binary files (like images or executables) might lead to errors or corruption if saved.

    Encoding: The app tries to auto-detect file encoding but defaults to UTF-8. If you encounter garbled text, the file might use an encoding the app couldn't detect correctly. Saving is done using the detected encoding (for Save) or UTF-8 (for Save Preview As).
