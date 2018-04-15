# STAGING

The proposed system would be a mobile and desktop compatible web app. It would offer the following functions:

- Allow QuOffice staff to create a &quot;session&quot; via an admin panel. The session would specify the question that participants must respond to via post-its, and specify the unit of measurement for the timeline&#39;s timeseries: a numerical age or MM/YY date, to allow for different types of timeline questions like &quot;How has your group represented gender and sexuality over the course of the calendar year&quot; (a MM/YY timestamp) versus &quot;how have you learned about gender and sexuality across your life&quot; (a numerical age timestamp).
- Allow participants to contribute to a specific session over a mobile-compatible interface, type the content for their post-its, and plot each post-it along a timeline.
- Have a well-designed view that visually represents the timeline and that can be projected on a screen at the front of the room. This view would live-update as post-its are submitted.
- Have a mobile-compatible version of the same visual timeline so that users can examine the curated submissions more closely on their own phones and scroll through them.
- Allow the QuOffice to &quot;close&quot; the session via the admin panel so that it doesn&#39;t accept any more submissions.
- Work on a limited budget: either use Azure&#39;s services that are free for students or constrain the budget to a specific amount. Warn the QuOffice when the storage usage is nearing a budget constraint.
- Allow the QuOffice to export past session data as a CSV via the admin panel and delete it from the server to free up space for future sessions.
- Bonus: allow the QuOffice to optionally enable &quot;monitoring&quot;, so that submitted post-its only appear on the visual timeline after they&#39;re screened by another staffer in live-time. Since we sometimes conduct workshops with groups that aren&#39;t ready to maturely engage with our content, we would want to preserve the integrity of the space by not letting the digital medium&#39;s distance enable people&#39;s irresponsible sides.


## STAGE 1
- Set up database to store session and post-it info
- Build a basic website with a text-based UI that allows admin to administer sessions, and users to respond.


## STAGE 2
- Make the UI from stage 1 mobile-compatible.


## STAGE 3
- Format each session's timeline view nicely -- pretty UI!
- Make the timeline view mobile compatible


## STAGE 4
- Have the timeline live-update with delta updates on both web and mobile


## STAGE 5
- Allow the QuOffice to export past session data as a CSV via the admin panel and delete it from the server to free up space for future sessions.


## STAGE 6
- Work on a limited budget: either use Azure&#39;s services that are free for students or constrain the budget to a specific amount. Warn the QuOffice when the storage usage is nearing a budget constraint.
