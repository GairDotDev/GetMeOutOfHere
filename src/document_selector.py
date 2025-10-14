"""
Document selector for choosing the right resume and cover letter for each job.
"""

import os
from typing import Dict, Tuple, Optional


class DocumentSelector:
    """Selects appropriate resume and cover letter based on job characteristics."""
    
    def __init__(self, documents_config: Dict):
        """
        Initialize the document selector.
        
        Args:
            documents_config: Dictionary containing document paths and mappings
        """
        self.config = documents_config
        self.resumes_dir = documents_config.get('resumes_dir', './resumes')
        self.cover_letters_dir = documents_config.get('cover_letters_dir', './cover_letters')
        self.default_resume = documents_config.get('default_resume', 'resume_general.pdf')
        self.resume_mapping = documents_config.get('resume_mapping', {})
        self.cover_letter_mapping = documents_config.get('cover_letter_mapping', {})
    
    def select_documents(self, job: Dict) -> Tuple[Optional[str], Optional[str]]:
        """
        Select the most appropriate resume and cover letter for a job.
        
        Args:
            job: Dictionary containing job details
            
        Returns:
            Tuple of (resume_path, cover_letter_path)
        """
        resume_path = self._select_resume(job)
        cover_letter_path = self._select_cover_letter(job)
        
        return resume_path, cover_letter_path
    
    def _select_resume(self, job: Dict) -> Optional[str]:
        """
        Select the most appropriate resume for a job.
        
        Args:
            job: Dictionary containing job details
            
        Returns:
            Path to the selected resume, or None if not found
        """
        title = job.get('title', '').lower()
        description = job.get('description', '').lower()
        combined_text = f"{title} {description}"
        
        # Check for specific resume types based on keywords
        resume_keywords = {
            'backend': ['backend', 'server', 'api', 'django', 'flask', 'fastapi'],
            'frontend': ['frontend', 'react', 'vue', 'angular', 'javascript', 'typescript'],
            'fullstack': ['fullstack', 'full stack', 'full-stack'],
            'data_science': ['data scientist', 'machine learning', 'ml', 'ai', 'data analysis']
        }
        
        # Find best matching resume type
        for resume_type, keywords in resume_keywords.items():
            if any(keyword in combined_text for keyword in keywords):
                resume_file = self.resume_mapping.get(resume_type)
                if resume_file:
                    resume_path = os.path.join(self.resumes_dir, resume_file)
                    if os.path.exists(resume_path):
                        return resume_path
        
        # Fall back to default resume
        default_path = os.path.join(self.resumes_dir, self.default_resume)
        if os.path.exists(default_path):
            return default_path
        
        print(f"Warning: No resume found. Please ensure resumes exist in {self.resumes_dir}")
        return None
    
    def _select_cover_letter(self, job: Dict) -> Optional[str]:
        """
        Select the most appropriate cover letter for a job.
        
        Args:
            job: Dictionary containing job details
            
        Returns:
            Path to the selected cover letter, or None if not found
        """
        company = job.get('company', '').lower()
        description = job.get('description', '').lower()
        
        # Determine company type based on keywords
        if any(word in description for word in ['startup', 'early stage', 'series a', 'series b']):
            cover_letter_type = 'startup'
        elif any(word in description for word in ['enterprise', 'fortune 500', 'large company']):
            cover_letter_type = 'enterprise'
        else:
            cover_letter_type = 'generic'
        
        # Get cover letter file
        cover_letter_file = self.cover_letter_mapping.get(cover_letter_type, 'cover_letter_generic.pdf')
        cover_letter_path = os.path.join(self.cover_letters_dir, cover_letter_file)
        
        if os.path.exists(cover_letter_path):
            return cover_letter_path
        
        print(f"Warning: No cover letter found. Please ensure cover letters exist in {self.cover_letters_dir}")
        return None
    
    def validate_documents(self) -> bool:
        """
        Validate that required document directories and files exist.
        
        Returns:
            True if validation passes, False otherwise
        """
        errors = []
        
        # Check directories
        if not os.path.exists(self.resumes_dir):
            errors.append(f"Resumes directory not found: {self.resumes_dir}")
        
        if not os.path.exists(self.cover_letters_dir):
            errors.append(f"Cover letters directory not found: {self.cover_letters_dir}")
        
        # Check default resume
        default_resume_path = os.path.join(self.resumes_dir, self.default_resume)
        if not os.path.exists(default_resume_path):
            errors.append(f"Default resume not found: {default_resume_path}")
        
        if errors:
            for error in errors:
                print(f"Validation error: {error}")
            return False
        
        return True
