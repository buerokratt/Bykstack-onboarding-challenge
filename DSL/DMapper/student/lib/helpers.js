import fs from 'fs';
import path from 'path';

/**
 * Formats date values to a consistent format (YYYY-MM-DD)
 * @param {string|Date} dateString - Date to format
 * @returns {string} Formatted date string or empty string if invalid
 */
export function formatDate(dateString) {
  if (!dateString) return '';
  
  try {
    const date = new Date(dateString);
    if (isNaN(date.getTime())) return ''; // Invalid date check
    return date.toISOString().split('T')[0]; // YYYY-MM-DD format
  } catch (e) {
    console.error('Date formatting error:', e);
    return '';
  }
}

/**
 * Formats datetime values to a consistent format (YYYY-MM-DD HH:MM:SS)
 * @param {string|Date} dateTimeString - Datetime to format
 * @returns {string} Formatted datetime string or empty string if invalid
 */
export function formatDateTime(dateTimeString) {
  if (!dateTimeString) return '';
  
  try {
    const date = new Date(dateTimeString);
    if (isNaN(date.getTime())) return ''; // Invalid date check
    return date.toISOString().replace('T', ' ').substring(0, 19); // YYYY-MM-DD HH:MM:SS
  } catch (e) {
    console.error('Datetime formatting error:', e);
    return '';
  }
}

/**
 * Escapes values for CSV format
 * @param {any} value - Value to escape
 * @returns {string} CSV-escaped string
 */
export function escapeCSV(value) {
  if (value === null || value === undefined) return '';
  
  const stringValue = String(value).trim();
  // If value contains comma, quote, or newline, wrap in quotes and escape internal quotes
  if (/[",\n\r]/.test(stringValue)) {
    return `"${stringValue.replace(/"/g, '""')}"`;
  }
  return stringValue;
}

/**
 * Transforms student data object to CSV format and saves to file
 * @param {Object} input - Student data object or wrapper containing student data
 * @returns {Object} Object containing CSV string, file info, and success status
 */
export function return_student_to_csv(input) {
  // Handle both direct input and wrapped input cases
  const studentData = input.data || input;
  
  if (!studentData) {
    return { success: false, csv: '', error: 'No student data provided' };
  }

  try {
    // CSV header row
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
      escapeCSV(studentData.id),
      escapeCSV(studentData.firstName),
      escapeCSV(studentData.lastName),
      escapeCSV(studentData.email),
      escapeCSV(studentData.phone),
      formatDate(studentData.dateOfBirth),
      escapeCSV(studentData.gender),
      formatDate(studentData.enrollmentDate),
      escapeCSV(studentData.status),
      formatDateTime(studentData.createdAt),
      formatDateTime(studentData.updatedAt)
    ];
    
    // Create CSV content (header row + data row)
    const csvContent = [
      headers.join(','),
      values.join(',')
    ].join('\n');
    
    // Create filename using student ID
    const studentId = studentData.id || 'unknown';
    const fileName = `${studentId}.csv`;
    
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
        success: true,
        filePath: filePath,
        fileName: fileName
      };
    } catch (error) {
      console.error('Error saving CSV file:', error);
      return {
        csv: csvContent,
        success: false,
        error: 'Failed to save CSV file'
      };
    }
  } catch (error) {
    console.error('Error generating CSV:', error);
    return {
      success: false,
      csv: '',
      error: 'Failed to generate CSV'
    };
  }
}

/**
 * Validates if a string contains only letters, numbers, and underscores
 * @param {string} name - String to validate
 * @returns {boolean} True if string is valid
 */
export function isValidIntentName(name) {
  if (!name || typeof name !== 'string') return false;
  // Allows letters (any unicode letter), numbers, and underscores
  return /^[\p{L}\p{N}_]+$/u.test(name);
}