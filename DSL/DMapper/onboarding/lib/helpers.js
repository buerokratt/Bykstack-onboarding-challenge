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
    escapeCSV(studentData.firstName || ''),
    escapeCSV(studentData.lastName || ''),
    escapeCSV(studentData.email || ''),
    escapeCSV(studentData.phone || ''),
    escapeCSV(formatDate(studentData.dateOfBirth) || ''),
    escapeCSV(studentData.gender || ''),
    escapeCSV(formatDate(studentData.enrollmentDate) || ''),
    escapeCSV(studentData.status || ''),
    escapeCSV(formatDateTime(studentData.createdAt) || ''),
    escapeCSV(formatDateTime(studentData.updatedAt) || '')
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


export function isValidIntentName(name) {
  // Allows letters (any unicode letter), numbers, and underscores
  // Matches front-end validation with spaces replaced with underscores
  return /^[\p{L}\p{N}_]+$/u.test(name);
}
