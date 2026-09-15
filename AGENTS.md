# OMDA14: live teaching and novice review

Luis delivers the class live. Students have little experience with Git, Python, Streamlit or LLMs.

- Main is preparation before class. Student pages describe OMDA14 and the next action. Keep course provenance, old material, plans, solutions and verification under docente, outside student navigation.
- Start each exercise with the smallest useful program. Students add functionality alongside Luis. Do not replace a build exercise with an almost finished demo.
- Introduce one concept when it solves the current problem. Predictions precede observations and answers. Include short pauses controlled by Luis.
- Explain Git through what happens to the student's files. Specify where commands run and where code additions go. Preserve student work.
- Before publishing a new exercise or a material change to student navigation, run a read-only novice subagent review. Prime the reviewer as a beginner following Luis, starting only from student entry pages. Ask for unclear actions, undefined terms, accidental prerequisites, spoilers, pause points and what the student actually builds. Apply relevant feedback and repeat a bounded review after substantive corrections.
- Keep a concise review record in docente. A simulated review is not feedback from real students.
- Test the expected starter error and every cumulative build stage without credentials or network access. Runtime dependencies belong in requirements.txt.
