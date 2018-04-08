# CS262 Final Project Proposal

Harshita Gupta

In the Harvard College Office of BGLTQ Student Life&#39;s (QuOffice&#39;s) &quot;Thinking Queerly&quot; workshops, the facilitators prompt participants to interrogate ways in which they&#39;ve learned about normative gender and sexuality across their lifetimes. To this end, we lead two &quot;timeline activities&quot; which currently waste a lot of paper and are cumbersome to digitize and commit to institutional memory. For my final project, I would like to build a distributed system that facilitates the activity during the workshop and allows students to participate anonymously via their smartphones.

## The Activity

Traditionally, the activity is conducted by handing out post-its to the attendees and asking them to write down, on individual post-its, specific moments during which they learned about gender and sexuality across their lifetime. They then stick their 6-10 post-its on a whiteboard, plotting each post-it along a timeline of their life. Once participants are done adding their post-its to the timeline, the group gathers around the timeline and looks for trends/similarities across post-its. This process is currently very awkward and cumbersome since the entire group can&#39;t gather around the whiteboard and view the material in any efficient way.

## The Proposed System

The proposed system would be a mobile and desktop compatible web app. It would offer the following functions:

- Allow QuOffice staff to create a &quot;session&quot; via an admin panel. The session would specify the question that participants must respond to via post-its, and specify the unit of measurement for the timeline&#39;s timeseries: a numerical age or MM/YY date, to allow for different types of timeline questions like &quot;How has your group represented gender and sexuality over the course of the calendar year&quot; (a MM/YY timestamp) versus &quot;how have you learned about gender and sexuality across your life&quot; (a numerical age timestamp).
- Allow participants to contribute to a specific session over a mobile-compatible interface, type the content for their post-its, and plot each post-it along a timeline.
- Have a well-designed view that visually represents the timeline and that can be projected on a screen at the front of the room. This view would live-update as post-its are submitted.
- Have a mobile-compatible version of the same visual timeline so that users can examine the curated submissions more closely on their own phones and scroll through them.
- Allow the QuOffice to &quot;close&quot; the session via the admin panel so that it doesn&#39;t accept any more submissions.
- Work on a limited budget: either use Azure&#39;s services that are free for students or constrain the budget to a specific amount. Warn the QuOffice when the storage usage is nearing a budget constraint.
- Allow the QuOffice to export past session data as a CSV via the admin panel and delete it from the server to free up space for future sessions.
- Bonus: allow the QuOffice to optionally enable &quot;monitoring&quot;, so that submitted post-its only appear on the visual timeline after they&#39;re screened by another staffer in live-time. Since we sometimes conduct workshops with groups that aren&#39;t ready to maturely engage with our content, we would want to preserve the integrity of the space by not letting the digital medium&#39;s distance enable people&#39;s irresponsible sides.

## Distributed Systems Problems Tackled

- Working on a limited financial budget. This will require:
    - Finding an Azure/AWS/Google App Engine configuration that takes advantage of our @college email perks as much as possible.
    - Constraining the app&#39;s resource usage to work within the free account&#39;s constraints. (primarily storage, since workshops only have about 40 users at once)
- Concurrency: participants will be adding content to the timeline simultaneously during the course of the session. The system should handle this gracefully and update the live timeline gracefully as well.
- Immediate consistency: since this is a live workshop, the data will all be centralized and pushed to all users immediately.
- Live updates: we will need to implement an efficient delta updates scheme so that the live-updating of the timeline is quick and not a drain on the network, since workshops can often end up with &gt; 100 post-its. Sending all of the timeline to each participant&#39;s phone on a &quot;refresh&quot; would not scale well.
- Support multiple simultaneous workshops: as the QuOffice hopes to expand its offerings, if we do multiple simultaneous workshops during Opening Days, the system should support traffic to multiple active sessions at once.
- Anonymity: due to the sensitive nature of the content being collected, we should ensure that no IP information/identifying information is retained about submissions.

__Disclaimer__: As you might have guessed, Harshita is an intern at the QuOffice, and is excited to prototype this at work. She isn&#39;t getting paid to work on the project, but hopes to use it on the job at the office starting in the Fall. She hopes that that&#39;s okay!

__Questions for Professor Waldo__: is this appropriately scoped to be one person&#39;s final project, or is it too much/too little? Are one-person groups okay?
