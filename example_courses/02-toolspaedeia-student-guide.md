@start name
Toolspaedeia Student Guide
@end name

@start description
A comprehensive guide for students to maximize their learning experience on the Toolspaedeia platform. Learn how to navigate courses, utilize offline capabilities, and track your progress.
@end description

@start module
@start title
Getting Started with Toolspaedeia
@end title

@start description
Introduction to the platform, account setup, and the first steps toward learning.
@end description

@start content
## Welcome to Toolspaedeia

Toolspaedeia is designed as a "lean" educational environment. This means we prioritize content and accessibility over visual complexity.

### Your Dashboard

Upon logging in, you will find:
- **Browse Courses:** Explore available content.
- **My Courses:** Access materials you have already purchased.
- **User Preferences:** Customize your interface theme.

### Installing the PWA

To get the most out of the platform, we recommend installing it as a Progressive Web App (PWA).
1. Open the site in your mobile browser.
2. Look for the "Add to Home Screen" prompt or use the browser menu.
3. Once installed, you can access the app directly from your home screen, providing a more immersive experience and enabling offline support.
@end content

@start quiz
@start title
Quiz: Getting Started
@end title

@start description
Verify your understanding of the platform's basic features.
@end description

@start question
@start text
What is the primary benefit of installing Toolspaedeia as a PWA?
@end text

@start answer
@start text
It allows the app to be installed via the App Store.
@end text

@start is_correct
false
@end is_correct
@end answer

@start answer
@start text
It enables offline access to downloaded content and home screen shortcuts.
@end text

@start is_correct
true
@end is_correct
@end answer

@start answer
@start text
It increases the visual complexity of the interface.
@end text

@start is_correct
false
@end is_correct
@end answer
@end question
@end quiz
@end module

@start module
@start title
Using the Platform Offline
@end title

@start description
Understand how the offline mode works and how to ensure your courses are available without internet.
@end description

@start content
## How Offline Access Works

Toolspaedeia uses a Service Worker to cache the "App Shell" and the specific courses you have purchased.

### The Caching Process

When you visit a course module while online, the content is automatically saved in your browser's local cache. If you are in a region with unstable connectivity, we recommend:
1. Opening each module of your course once while you have a stable connection.
2. Waiting for the page to load completely.

## Identifying Offline State

When you are offline, a connectivity banner will appear at the top of the page:
*"You are currently offline. Click here for more details."*

In this mode, you can still read all cached modules and view your purchased courses, but interactive features like quizzes and progress markers will be disabled until you return online.
@end content

@start quiz
@start title
Quiz: Offline Capabilities
@end title

@start description
Check your knowledge of how the offline mode operates.
@end description

@start question
@start text
Which of the following actions is NOT possible while in offline mode?
@end text

@start answer
@start text
Reading a previously visited module.
@end text

@start is_correct
false
@end is_correct
@end answer

@start answer
@start text
Marking a module as complete.
@end text

@start is_correct
true
@end is_correct
@end answer

@start answer
@start text
Viewing the list of purchased courses.
@end text

@start is_correct
false
@end is_correct
@end answer
@end question
@end quiz
@end module

@start module
@start title
Tracking Progress and Quizzes
@end title

@start description
Learn how to evaluate your knowledge and keep track of your learning journey.
@end description

@start content
## Completing Modules

At the end of each module, you will find a "Mark as Complete" button. Clicking this allows you to track your progress within the course. This data is stored on the server and is visible on your course overview page as a percentage of completion.

## Taking Quizzes

Quizzes are designed to validate your understanding of the material.
- **Attempts:** You can attempt a quiz multiple times.
- **Best Grade:** The system tracks your best attempt, allowing you to strive for a perfect score.
- **Instant Feedback:** Upon submission, the system will highlight correct and incorrect answers, providing immediate learning opportunities.
@end content

@start quiz
@start title
Quiz: Progress and Validation
@end title

@start description
Verify your understanding of the progress tracking system.
@end description

@start question
@start text
How is the overall course progress calculated?
@end text

@start answer
@start text
Based on the time spent on each page.
@end text

@start is_correct
false
@end is_correct
@end answer

@start answer
@start text
By the ratio of modules marked as complete to the total number of modules.
@end text

@start is_correct
true
@end is_correct
@end answer

@start answer
@start text
It is determined by the final quiz score only.
@end text

@start is_correct
false
@end is_correct
@end answer
@end question
@end quiz
@end module
