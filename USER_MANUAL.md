# Assessment Management System - User Manual

## 📋 Table of Contents
1. [System Overview](#system-overview)
2. [Getting Started](#getting-started)
3. [Admin User Guide](#admin-user-guide)
4. [Candidate User Guide](#candidate-user-guide)
5. [Assessment Management](#assessment-management)
6. [Question Management](#question-management)
7. [User Management](#user-management)
8. [Analytics & Reporting](#analytics--reporting)
9. [Troubleshooting](#troubleshooting)
10. [Security & Best Practices](#security--best-practices)

---




## 🎯 System Overview

The Assessment Management System is a comprehensive web-based platform designed for creating, administering, and evaluating various types of assessments. The system supports multiple user roles with different access levels and capabilities.

### Key Features
- **Multi-Role Access**: Admin and Candidate roles with distinct permissions
- **Assessment Types**: Support for IQ tests, cultural assessments, and custom evaluations
- **Question Formats**: Multiple choice, true/false, and short answer questions
- **Real-Time Assessment**: Timer-based assessments with auto-save functionality
- **Mobile Responsive**: Fully optimized for desktop, tablet, and mobile devices
- **Analytics & Reporting**: Comprehensive performance tracking and analysis
- **Bulk Operations**: Import/export questions and results

### User Roles

#### Admin Users
- **Full System Access**: Complete control over all system functions
- **Assessment Management**: Create, edit, delete, and configure assessments
- **Question Management**: Manage question bank with various formats
- **User Management**: Monitor candidate activities and sessions
- **Analytics Access**: View detailed reports and performance statistics
- **Results Access**: Exclusive access to detailed assessment results

#### Candidate Users
- **Assessment Taking**: Access to assigned assessments
- **Progress Tracking**: View assessment history and completion status
- **Profile Management**: Basic profile information management
- **Session Management**: Resume incomplete assessments
- **Restricted Results**: Only see completion confirmation, no detailed scores

---

## 🚀 Getting Started

### Accessing the System

#### For Admins
1. **Navigate to**: `https://bit.ly/TMHRTest`
2. **Login with**: Username and password
3. **Access Dashboard**: Automatically redirected to admin dashboard

#### For Candidates
1. **Navigate to**: `https://bit.ly/TMHRTest`
2. **Login with**: First name and last name
3. **Access Portal**: Automatically redirected to candidate portal

### First-Time Setup (Admin)

#### Creating Your First Assessment
1. **Access Admin Dashboard**
2. **Click "Create Assessment"** in Quick Actions
3. **Fill Assessment Details**:
   - Name: Descriptive assessment title
   - Description: Brief overview of the assessment
   - Assessment Type: Select from available designations
   - Time Limit: Set appropriate time constraints
   - Pass Threshold: Define passing percentage
   - Max Attempts: Set attempt limitations
4. **Save Assessment**

#### Adding Questions
1. **Navigate to Questions** section
2. **Click "Create Question"**
3. **Select Question Type**:
   - **Multiple Choice**: Choose from predefined options
   - **True/False**: Binary choice questions
   - **Short Answer**: Text-based responses
4. **Fill Question Details**:
   - Question text
   - Options (for MCQ)
   - Correct answer
   - Points value
   - Category (optional)
5. **Save Question**

#### Linking Questions to Assessments
1. **Go to Assessment Details**
2. **Click "Add Questions"**
3. **Select Questions** that match the assessment type
4. **Set Question Order** and point values
5. **Save Configuration**

---

## 👨‍💼 Admin User Guide

### Admin Dashboard

The admin dashboard provides a comprehensive overview of system activity and quick access to key functions.

#### Dashboard Components
- **Statistics Cards**: Total assessments, questions, users, and sessions
- **Quick Actions**: Direct links to common tasks
- **Recent Activity**: Latest assessment sessions and user activities
- **Assessment Type Distribution**: Visual breakdown of assessment categories

#### Quick Actions Available
- **Create Assessment**: Start a new assessment
- **Assign Assessment**: Assign assessments to candidates
- **Manage Questions**: Access question bank
- **View Analytics**: Access detailed reports
- **Export Results**: Download assessment data

### Assessment Management

#### Creating Assessments

**Step 1: Basic Information**
- **Name**: Clear, descriptive title
- **Description**: Detailed explanation of assessment purpose
- **Assessment Type**: Select appropriate designation (IQ, Cultural, etc.)
- **Instructions**: Specific guidelines for candidates

**Step 2: Configuration**
- **Time Limit**: Set reasonable time constraints (default: 60 minutes)
- **Pass Threshold**: Define passing percentage (0-100%)
- **Max Attempts**: Limit retake attempts (default: 1)
- **Randomize Questions**: Enable/disable question randomization
- **Show Results**: Choose whether to show results immediately

**Step 3: Question Assignment**
- **Add Existing Questions**: Select from question bank
- **Bulk Import**: Upload questions via Excel/CSV
- **Question Order**: Arrange questions in desired sequence
- **Point Allocation**: Assign custom point values

#### Managing Existing Assessments

**Viewing Assessment Details**
- **Overview**: Basic information and statistics
- **Questions**: List of assigned questions with order
- **Sessions**: Assessment attempts and results
- **Analytics**: Performance metrics and trends

**Editing Assessments**
- **Modify Settings**: Update time limits, thresholds, etc.
- **Add/Remove Questions**: Adjust question composition
- **Update Instructions**: Modify candidate guidelines
- **Change Status**: Activate/deactivate assessments

**Deleting Assessments**
- **Permanent Deletion**: Assessments are permanently removed
- **Impact Warning**: System shows affected sessions and data
- **Confirmation Required**: Multiple confirmation steps

### Question Management

#### Creating Questions

**Multiple Choice Questions**
1. **Select "Multiple Choice"** type
2. **Enter Question Text**: Clear, unambiguous question
3. **Add Options**: Provide 2-6 answer choices
4. **Mark Correct Answer**: Select the right option
5. **Set Points**: Assign point value (default: 1)
6. **Add Explanation**: Optional explanation for correct answer

**True/False Questions**
1. **Select "True/False"** type
2. **Enter Question Text**: Clear statement
3. **Set Correct Answer**: True or False
4. **Add Explanation**: Why the answer is correct

**Short Answer Questions**
1. **Select "Short Answer"** type
2. **Enter Question Text**: Open-ended question
3. **Set Expected Answer**: Model answer for reference
4. **Note**: Requires manual review for scoring

#### Question Bank Management

**Organizing Questions**
- **Categories**: Group questions by topic or skill
- **Assessment Types**: Filter by designation
- **Status**: Active/inactive questions
- **Search**: Find specific questions quickly

**Bulk Operations**
- **Import Questions**: Upload Excel/CSV files
- **Export Questions**: Download question bank
- **Bulk Delete**: Remove multiple questions
- **Bulk Update**: Modify multiple questions

### User Management

#### Monitoring Candidate Activity
- **Session Tracking**: View all assessment attempts
- **Progress Monitoring**: Track completion rates
- **Performance Analysis**: Individual and aggregate scores
- **Access Control**: Manage candidate permissions

#### Assigning Assessments
1. **Select Candidate**: Choose from user list
2. **Choose Assessment**: Pick appropriate assessment
3. **Set Parameters**: Configure attempt limits
4. **Send Notification**: Inform candidate of assignment

### Analytics & Reporting

#### Performance Analytics
- **Score Distributions**: Visual representation of results
- **Completion Rates**: Assessment completion statistics
- **Time Analysis**: Average completion times
- **Question Analysis**: Individual question performance

#### Export Options
- **Excel Export**: Detailed results in spreadsheet format
- **PDF Reports**: Formatted reports for printing
- **CSV Data**: Raw data for external analysis
- **Custom Reports**: Filtered data exports

#### Key Metrics
- **Overall Performance**: System-wide statistics
- **Assessment-Specific**: Individual assessment metrics
- **User Performance**: Individual candidate tracking
- **Trend Analysis**: Performance over time

---

## 👤 Candidate User Guide

### Candidate Portal

The candidate portal provides a user-friendly interface for taking assessments and tracking progress.

#### Portal Features
- **Available Assessments**: List of assigned assessments
- **Progress Tracking**: Current assessment status
- **Session Management**: Resume incomplete assessments
- **Profile Information**: Basic user details

### Taking Assessments

#### Starting an Assessment
1. **Select Assessment**: Choose from available assessments
2. **Review Details**: Check time limit, question count, pass threshold
3. **Read Instructions**: Review assessment guidelines
4. **Click "Start Assessment"**: Begin the assessment session

#### During Assessment
- **Timer Display**: Real-time countdown timer
- **Question Navigation**: Move between questions
- **Auto-Save**: Answers are automatically saved
- **Progress Indicator**: Visual progress tracking
- **Question Types**: Different formats as configured

#### Question Types

**Multiple Choice Questions**
- **Format**: Select one answer from options
- **Navigation**: Use radio buttons to select
- **Review**: Can change answers before submission

**True/False Questions**
- **Format**: Choose True or False
- **Simple**: Binary choice selection
- **Quick**: Fast to answer

**Short Answer Questions**
- **Format**: Text input field
- **Flexible**: Open-ended responses
- **Manual Review**: Requires admin evaluation

#### Assessment Completion
1. **Review Answers**: Check all responses
2. **Submit Assessment**: Final submission
3. **Confirmation**: Receive completion confirmation
4. **No Results**: Detailed results are admin-only

### Session Management

#### Resuming Assessments
- **Incomplete Sessions**: Continue where you left off
- **Auto-Save**: Previous answers are preserved
- **Time Tracking**: Remaining time is maintained
- **Seamless Experience**: No data loss

#### Assessment History
- **Completed Assessments**: List of finished assessments
- **Completion Dates**: When assessments were taken
- **Status Tracking**: Pass/fail status (if available)
- **Attempt Information**: Number of attempts used

---

## 📊 Assessment Management

### Assessment Types

#### IQ Assessments
- **Purpose**: Measure cognitive abilities
- **Question Types**: Logic, reasoning, pattern recognition
- **Scoring**: Objective scoring with clear answers
- **Time Limits**: Typically 30-60 minutes

#### Cultural Assessments
- **Purpose**: Evaluate cultural knowledge and fit
- **Question Types**: Cultural scenarios, values, behaviors
- **Scoring**: May include subjective evaluation
- **Time Limits**: Usually 20-45 minutes

#### Custom Assessments
- **Purpose**: Specific organizational needs
- **Question Types**: Tailored to requirements
- **Scoring**: Custom scoring algorithms
- **Time Limits**: Variable based on complexity

### Assessment Configuration

#### Time Management
- **Time Limits**: Set appropriate constraints
- **Auto-Submit**: Automatic submission when time expires
- **Timer Display**: Real-time countdown for candidates
- **Grace Period**: Optional buffer time

#### Scoring System
- **Point Allocation**: Custom points per question
- **Pass Threshold**: Minimum percentage to pass
- **Weighted Scoring**: Different question weights
- **Bonus Points**: Additional scoring options

#### Security Features
- **Attempt Limits**: Prevent excessive retakes
- **Randomization**: Question and option shuffling
- **Session Tracking**: Monitor assessment sessions
- **Access Control**: Restrict unauthorized access

---

## ❓ Question Management

### Question Bank Organization

#### Categories
- **Topic-Based**: Group by subject matter
- **Skill Areas**: Specific competencies
- **Assessment Types**: IQ, cultural

#### Question Quality
- **Clarity**: Clear, unambiguous language
- **Relevance**: Appropriate for assessment type
- **Difficulty**: Appropriate complexity level
- **Validity**: Measures intended skills

### Question Creation Best Practices

#### Multiple Choice Questions
- **Clear Stem**: Unambiguous question text
- **Plausible Options**: All options should be reasonable
- **Single Correct Answer**: Only one right answer
- **Avoid Negatives**: Minimize negative phrasing


#### Short Answer Questions
- **Clear Expectations**: Specify expected response length
- **Rubric Development**: Create scoring criteria
- **Model Answers**: Provide reference responses
- **Manual Review**: Plan for human evaluation

---

## 👥 User Management

### Admin User Administration

#### Creating Admin Users
- **Authorized Emails**: Only specific emails can create admin accounts
- **Role Assignment**: Admin or HR Admin roles
- **Permission Levels**: Different access levels
- **Security Validation**: Email verification required

#### Admin Permissions
- **Full Access**: Complete system control
- **Assessment Management**: Create and modify assessments
- **User Management**: Monitor and manage candidates
- **Analytics Access**: View all reports and statistics

### Candidate User Management

#### Candidate Registration
- **Name-Based Login**: First and last name authentication
- **Simple Process**: Minimal registration requirements
- **Automatic Assignment**: Based on assessment assignments
- **Profile Management**: Basic information storage

#### Candidate Monitoring
- **Session Tracking**: Monitor assessment attempts
- **Progress Reports**: Track completion status
- **Performance Analysis**: Individual and aggregate data
- **Access Control**: Manage assessment access

---

## 📈 Analytics & Reporting

### Performance Analytics

#### System Overview
- **Total Assessments**: Number of active assessments
- **Total Questions**: Questions in the bank
- **Total Users**: Registered candidates
- **Total Sessions**: Assessment attempts

#### Assessment Performance
- **Completion Rates**: Percentage of started assessments completed
- **Average Scores**: Mean performance across assessments
- **Pass Rates**: Percentage of candidates passing
- **Time Analysis**: Average completion times

#### Question Analysis
- **Difficulty Levels**: Question performance metrics
- **Response Patterns**: Common answer choices
- **Success Rates**: Percentage of correct answers
- **Time per Question**: Average time spent

### Report Generation

#### Export Formats
- **Excel Reports**: Comprehensive spreadsheet data
- **PDF Reports**: Formatted for printing and sharing
- **CSV Data**: Raw data for external analysis
- **Custom Reports**: Filtered data exports

#### Report Types
- **Individual Reports**: Candidate-specific performance
- **Assessment Reports**: Assessment-specific analytics
- **Comparative Reports**: Cross-assessment analysis
- **Trend Reports**: Performance over time

#### Data Privacy
- **Admin-Only Access**: Detailed results restricted to admins
- **Candidate Privacy**: Candidates see only completion status
- **Secure Storage**: Encrypted data storage
- **Access Logging**: Track who views reports

---

## 🔧 Troubleshooting

### Common Issues

#### Login Problems
**Issue**: Cannot log in as admin
- **Solution**: Verify email is in authorized admin list
- **Check**: Username and password are correct
- **Contact**: System administrator for access

**Issue**: Cannot log in as candidate
- **Solution**: Use first name and last name exactly as registered
- **Check**: Name spelling and capitalization
- **Contact**: Admin for account verification

#### Assessment Issues
**Issue**: Assessment shows no questions
- **Solution**: Check question links in admin panel
- **Action**: Run deployment setup command
- **Contact**: Admin for technical support

**Issue**: Timer not working
- **Solution**: Refresh page and restart assessment
- **Check**: Internet connection stability
- **Action**: Contact admin if problem persists

#### Technical Problems
**Issue**: Page not loading
- **Solution**: Check internet connection
- **Action**: Clear browser cache and cookies
- **Contact**: Technical support if issue continues

**Issue**: Mobile display issues
- **Solution**: Use responsive design features
- **Action**: Rotate device or use desktop mode
- **Check**: Browser compatibility

### Error Messages

#### Common Error Codes
- **404 Error**: Page not found - check URL
- **500 Error**: Server error - contact administrator
- **403 Error**: Access denied - check permissions
- **Session Expired**: Re-login required


---

## 🔒 Security & Best Practices

### Security Features

#### Access Control
- **Role-Based Permissions**: Different access levels
- **Email Authorization**: Admin access restrictions
- **Session Management**: Secure session handling
- **Password Security**: Strong password requirements

#### Data Protection
- **Encryption**: Secure data transmission
- **Backup Systems**: Regular data backups
- **Access Logging**: Track system access
- **Privacy Controls**: Candidate data protection

### Best Practices

#### For Admins
- **Regular Backups**: Maintain data backups
- **User Monitoring**: Monitor system activity
- **Security Updates**: Keep system updated
- **Access Review**: Regular permission audits

#### For Candidates
- **Secure Login**: Use secure devices and networks
- **Session Management**: Log out after sessions
- **Data Privacy**: Protect personal information
- **Report Issues**: Report security concerns

#### System Maintenance
- **Regular Updates**: Keep software current
- **Performance Monitoring**: Track system performance
- **Security Audits**: Regular security reviews
- **User Training**: Provide user education

### Data Privacy

#### Candidate Rights
- **Data Access**: Request personal data
- **Data Correction**: Update personal information
- **Data Deletion**: Request data removal
- **Privacy Information**: Understand data usage

#### Admin Responsibilities
- **Data Protection**: Secure candidate information
- **Access Control**: Limit data access
- **Audit Trails**: Maintain access logs
- **Compliance**: Follow privacy regulations

---

## 📞 Support & Contact

### Getting Help

#### Technical Support
- **Email**: Contact system administrator
- **Documentation**: Refer to this manual
- **Online Resources**: Check system help section
- **Training Materials**: Access user training resources

#### Common Support Requests
- **Account Access**: Login and permission issues
- **Assessment Problems**: Technical assessment issues
- **Data Questions**: Information about data and reports
- **Feature Requests**: Suggestions for improvements

### System Information

#### Version Details
- **Current Version**: 2025.1
- **Last Updated**: January 2025
- **Compatibility**: Modern web browsers
- **Mobile Support**: Full mobile responsiveness

#### System Requirements
- **Browser**: Chrome, Firefox, Safari, Edge (latest versions)
- **Internet**: Stable internet connection
- **Device**: Desktop, tablet, or mobile device
- **JavaScript**: Enabled for full functionality

---

## 📝 Appendix

### Keyboard Shortcuts
- **Ctrl+S**: Save (during assessment)
- **F5**: Refresh page
- **Ctrl+F**: Find text
- **Esc**: Close dialogs

### Glossary
- **Assessment**: A test or evaluation with questions
- **Session**: Individual assessment attempt
- **Question Bank**: Collection of available questions
- **Analytics**: Performance data and statistics
- **Dashboard**: Main control panel for admins
- **Portal**: Main interface for candidates

### Quick Reference

#### Admin Quick Actions
1. **Create Assessment**: Dashboard → Quick Actions → Create Assessment
2. **Add Questions**: Questions → Create Question
3. **View Results**: Analytics → Assessment Results
4. **Export Data**: Analytics → Export Options

#### Candidate Quick Actions
1. **Start Assessment**: Portal → Available Assessments → Start
2. **Continue Assessment**: Portal → Continue Assessment
3. **View History**: Portal → Assessment History
4. **Update Profile**: Portal → Profile Settings

---

*This user manual is designed to help users effectively navigate and utilize the Assessment Management System. For additional support or questions, please contact your system administrator.*

**Last Updated**: January 2025  
**Version**: 2025.1  
**System**: Assessment Management System
