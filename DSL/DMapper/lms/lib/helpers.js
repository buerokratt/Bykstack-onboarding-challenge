import fs from 'fs';
import path from 'path';

/**
 * Formats date values to a consistent format (YYYY-MM-DD)
 */
export function formatDate(dateString) {
  if (!dateString) return '';
  try {
    const date = new Date(dateString);
    return date.toISOString().split('T')[0]; // YYYY-MM-DD format
  } catch (e) {
    return dateString;
  }
}

/**
 * Formats datetime values to a consistent format
 */
export function formatDateTime(dateTimeString) {
  if (!dateTimeString) return '';
  try {
    const date = new Date(dateTimeString);
    return date.toISOString().replace('T', ' ').substr(0, 19); // YYYY-MM-DD HH:MM:SS
  } catch (e) {
    return dateTimeString;
  }
}

/**
 * Escapes special characters for CSV output
 */
export function escapeCSV(value) {
  if (value === null || value === undefined) return '';
  
  const stringValue = String(value);
  // If value contains comma, quote, or newline, wrap in quotes and escape internal quotes
  if (/[",\n\r]/.test(stringValue)) {
    return `"${stringValue.replace(/"/g, '""')}"`;
  }
  return stringValue;
}

/**
 * Transforms student data object to CSV format and saves to file
 * This function is called directly by the datamapper service
 */
export function return_student_to_csv(input) {
  const studentData = input.data || input;
  
  // CSV header based on the provided schema
  const headers = [
    'ID',
    'First Name',
    'Last Name',
    'Email',
    'Phone',
    'Date of Birth',
    'Gender',
    'Enrollment Date',
    'Status',
    'Created At',
    'Updated At'
  ];
  
  // Map student properties to CSV row values
  const values = [
    escapeCSV(studentData.id || ''),
    escapeCSV(studentData.first_name || ''),
    escapeCSV(studentData.last_name || ''),
    escapeCSV(studentData.email || ''),
    escapeCSV(studentData.phone || ''),
    escapeCSV(formatDate(studentData.date_of_birth) || ''),
    escapeCSV(studentData.gender || ''),
    escapeCSV(formatDate(studentData.enrollment_date) || ''),
    escapeCSV(studentData.status || ''),
    escapeCSV(formatDateTime(studentData.created_at) || ''),
    escapeCSV(formatDateTime(studentData.updated_at) || '')
  ];
  
  // Create CSV content (header row + data row)
  const csvContent = [
    headers.join(','),
    values.join(',')
  ].join('\n');
  
  // Create a unique filename with timestamp and student email
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const sanitizedEmail = studentData.email.replace(/[@.]/g, '_');
  const fileName = `student_${sanitizedEmail}_${timestamp}.csv`;
  
  // Save file to shared volume directory
  const exportDir = '/shared';
  
  try {
    // Create directory if it doesn't exist
    if (!fs.existsSync(exportDir)) {
      fs.mkdirSync(exportDir, { recursive: true });
    }
    
    const filePath = path.join(exportDir, fileName);
    fs.writeFileSync(filePath, csvContent);
    
    return { 
      csv: csvContent,
      rowCount: 1,
      success: true,
      filePath: filePath,
      fileName: fileName
    };
  } catch (error) {
    console.error('Error saving CSV file:', error);
    return { 
      csv: csvContent,
      rowCount: 1,
      success: true,
      error: 'Failed to save CSV file'
    };
  }
}

/**
 * Transforms multiple student records to CSV and saves to file
 * This function is called directly by the datamapper service
 */
export function return_students_to_csv(input) {
  let studentsArray = [];
  
  if (Array.isArray(input)) {
    studentsArray = input;
  } else if (input.data && Array.isArray(input.data)) {
    studentsArray = input.data;
  } else {
    studentsArray = [input.data || input];
  }
  
  // CSV header based on the provided schema
  const headers = [
    'ID',
    'First Name',
    'Last Name',
    'Email',
    'Phone',
    'Date of Birth',
    'Gender',
    'Enrollment Date',
    'Status',
    'Created At',
    'Updated At'
  ];
  
  // Create rows for each student
  const rows = studentsArray.map(student => {
    return [
      escapeCSV(student.id || ''),
      escapeCSV(student.first_name || ''),
      escapeCSV(student.last_name || ''),
      escapeCSV(student.email || ''),
      escapeCSV(student.phone || ''),
      escapeCSV(formatDate(student.date_of_birth) || ''),
      escapeCSV(student.gender || ''),
      escapeCSV(formatDate(student.enrollment_date) || ''),
      escapeCSV(student.status || ''),
      escapeCSV(formatDateTime(student.created_at) || ''),
      escapeCSV(formatDateTime(student.updated_at) || '')
    ].join(',');
  });
  
  // Combine header and data rows
  const csvContent = [
    headers.join(','),
    ...rows
  ].join('\n');
  
  // Create a unique filename with timestamp
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const fileName = `students_export_${timestamp}.csv`;
  
  // Save file to shared volume directory
  const exportDir = '/shared';
  
  try {
    // Create directory if it doesn't exist
    if (!fs.existsSync(exportDir)) {
      fs.mkdirSync(exportDir, { recursive: true });
    }
    
    const filePath = path.join(exportDir, fileName);
    fs.writeFileSync(filePath, csvContent);
    
    return { 
      csv: csvContent,
      rowCount: studentsArray.length,
      success: true,
      filePath: filePath,
      fileName: fileName
    };
  } catch (error) {
    console.error('Error saving CSV file:', error);
    return { 
      csv: csvContent,
      rowCount: studentsArray.length,
      success: true,
      error: 'Failed to save CSV file'
    };
  }
}

/**
 * Validates student data based on schema requirements
 */
export function validateStudentData(student) {
  if (!student) {
    return { 
      isValid: false, 
      missingFields: ['all fields'] 
    };
  }
  
  const requiredFields = ['first_name', 'last_name', 'email', 'enrollment_date'];
  const missingFields = requiredFields.filter(field => !student[field]);
  
  return {
    isValid: missingFields.length === 0,
    missingFields: missingFields
  };
}

export function isValidIntentName(name) {
  // Allows letters (any unicode letter), numbers, and underscores
  // Matches front-end validation with spaces replaced with underscores
  return /^[\p{L}\p{N}_]+$/u.test(name);
}