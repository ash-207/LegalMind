
from summarizer import LegalSummarizer

s = LegalSummarizer(
    backend="openai",
    api_key="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",    model="llama-3.1-8b-instant",
    base_url="https://api.groq.com/openai/v1"
)

# summary = s.summarize(
#     "The defendant must submit evidence within 14 days. "
#     "Next hearing is March 15. Judge orders prosecution "
#     "to file charge sheet under IPC 420."
# )

summary = s.summarize("""
[00:00] Judge Sharma: This court is now in session for Case No. CRL/2024/447, 
State of Maharashtra versus Ramesh Gupta, pertaining to allegations under 
IPC Section 420 and 406 relating to cheating and criminal breach of trust.

[00:30] Judge Sharma: Mr. Mehta, you represent the defendant. Are you prepared 
to proceed today?

[01:00] Lawyer Mehta (Defense): Yes, Your Honour. However, I must bring to 
the court's attention that the prosecution has failed to submit the forensic 
audit report that was ordered in the previous hearing dated January 10th, 2024.

[01:30] Prosecutor Kulkarni: Your Honour, the forensic audit is still ongoing. 
The chartered accountant firm engaged for this purpose has requested an 
additional 3 weeks to complete the analysis of approximately 2,400 financial 
transactions spanning across 6 bank accounts.

[02:00] Judge Sharma: This is highly irregular. The court had clearly directed 
submission within 30 days. We are now 47 days past that deadline. 
I am issuing a strict warning to the prosecution. Any further delays will 
result in adverse inference being drawn.

[02:45] Lawyer Mehta: Your Honour, given this delay, I request that my client 
be granted bail. He has been in judicial custody for 63 days and the 
prosecution's repeated delays are causing grave prejudice to the defendant.

[03:10] Prosecutor Kulkarni: We strongly oppose bail. The defendant is a 
flight risk. He holds two passports and has financial assets abroad. 
Furthermore, there are 14 witnesses who may be intimidated if bail is granted.

[03:40] Judge Sharma: I note both arguments. Regarding bail, I will hear 
detailed arguments on the next date. The defendant's passport shall remain 
deposited with this court until further orders.

[04:00] Judge Sharma: Regarding the forensic report, I am directing the 
prosecution to submit the completed report no later than February 28th, 2024. 
Failure to do so will result in the court proceeding ex-parte on this matter.

[04:30] Lawyer Mehta: Your Honour, I also wish to place on record that the 
charge sheet filed by the prosecution does not mention the role of co-accused 
Priya Sharma, who was equally involved in the alleged transactions. 
We request the court to direct investigation into her role as well.

[05:00] Prosecutor Kulkarni: Co-accused Priya Sharma is currently absconding. 
An FIR has been registered and a non-bailable warrant has been issued by 
the jurisdictional magistrate court.

[05:20] Judge Sharma: The court takes note. The investigating officer shall 
file a status report on the arrest of the absconding accused within 7 days.

[05:45] Judge Sharma: To summarize today's directions: One, prosecution to 
submit forensic audit report by February 28th 2024. Two, investigating officer 
to submit status report on absconding accused within 7 days. Three, defendant's 
passport to remain deposited. Four, bail application to be heard on next date.
Next hearing is scheduled for February 15th, 2024 at 11:00 AM in Court No. 4.
Court is adjourned.
""")

print(s.to_text(summary))