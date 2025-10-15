"""
Job scoring system to evaluate job postings based on user preferences.
"""

from typing import Dict, List, Any
import re


class JobScorer:
    """Scores job postings based on weighted criteria."""
    
    def __init__(self, weights: Dict[str, float], preferences: Dict[str, Any]):
        """
        Initialize the job scorer.
        
        Args:
            weights: Dictionary of scoring weights for different criteria
            preferences: User preferences for job matching
        """
        self.weights = weights
        self.preferences = preferences
    
    def score_job(self, job: Dict[str, Any]) -> float:
        """
        Calculate weighted score for a job posting.
        
        Args:
            job: Dictionary containing job details
            
        Returns:
            Score between 0 and 10
        """
        scores = {
            'keyword_match': self._score_keyword_match(job),
            'salary_match': self._score_salary_match(job),
            'location_preference': self._score_location(job),
            'company_rating': self._score_company_rating(job),
            'role_seniority': self._score_role_seniority(job),
            'benefits': self._score_benefits(job)
        }
        
        # Calculate weighted sum
        total_score = sum(
            scores[criterion] * self.weights[criterion]
            for criterion in scores.keys()
        )
        
        # Scale to 0-10
        final_score = total_score * 10
        
        return round(final_score, 2)
    
    def _score_keyword_match(self, job: Dict[str, Any]) -> float:
        """
        Score based on keyword matching with required and nice-to-have skills.
        
        Returns:
            Score between 0 and 1
        """
        description = job.get('description', '').lower()
        title = job.get('title', '').lower()
        combined_text = f"{title} {description}"
        
        required_skills = self.preferences.get('required_skills', [])
        nice_to_have = self.preferences.get('nice_to_have_skills', [])
        
        # Check required skills
        required_matches = sum(
            1 for skill in required_skills
            if skill.lower() in combined_text
        )
        
        # Check nice-to-have skills
        nice_matches = sum(
            1 for skill in nice_to_have
            if skill.lower() in combined_text
        )
        
        # Score based on matches
        if not required_skills:
            required_score = 1.0
        else:
            required_score = required_matches / len(required_skills)
        
        if not nice_to_have:
            nice_score = 0
        else:
            nice_score = nice_matches / len(nice_to_have)
        
        # Weight required skills more heavily (70% required, 30% nice-to-have)
        return (required_score * 0.7) + (nice_score * 0.3)
    
    def _score_salary_match(self, job: Dict[str, Any]) -> float:
        """
        Score based on salary alignment with expectations.
        
        Returns:
            Score between 0 and 1
        """
        salary_min = job.get('salary_min')
        salary_max = job.get('salary_max')
        
        if not salary_min and not salary_max:
            # No salary info, give neutral score
            return 0.5
        
        target = self.preferences.get('target_salary')
        min_acceptable = self.preferences.get('min_salary')
        max_acceptable = self.preferences.get('max_salary')
        
        # Use average if both min and max provided
        if salary_min and salary_max:
            job_salary = (salary_min + salary_max) / 2
        else:
            job_salary = salary_min or salary_max
        
        # Score based on how close to target
        if job_salary < min_acceptable:
            return 0.0
        elif job_salary > max_acceptable:
            return 0.5  # Still okay, just higher than expected
        elif job_salary >= target:
            # Score increases as we get closer to target from above
            return 1.0
        else:
            # Score based on distance from min to target
            return (job_salary - min_acceptable) / (target - min_acceptable)
    
    def _score_location(self, job: Dict[str, Any]) -> float:
        """
        Score based on location preferences.
        
        Returns:
            Score between 0 and 1
        """
        job_location = job.get('location', '').lower()
        preferred_locations = [
            loc.lower() for loc in self.preferences.get('preferred_locations', [])
        ]
        
        if not preferred_locations:
            return 1.0
        
        # Check if job location matches any preferred location
        for preferred in preferred_locations:
            if preferred in job_location or job_location in preferred:
                return 1.0
        
        # Partial match gets partial score
        return 0.3
    
    def _score_company_rating(self, job: Dict[str, Any]) -> float:
        """
        Score based on company rating/reputation.
        
        Returns:
            Score between 0 and 1
        """
        rating = job.get('company_rating')
        
        if rating is None:
            # No rating available, give neutral score
            return 0.5
        
        # Assuming rating is on 0-5 scale
        return min(rating / 5.0, 1.0)
    
    def _score_role_seniority(self, job: Dict[str, Any]) -> float:
        """
        Score based on role seniority level match.
        
        Returns:
            Score between 0 and 1
        """
        title = job.get('title', '').lower()
        description = job.get('description', '').lower()
        combined_text = f"{title} {description}"
        
        experience_level = self.preferences.get('experience_level', 'mid').lower()
        
        # Define seniority indicators
        seniority_keywords = {
            'junior': ['junior', 'entry', 'associate', 'jr'],
            'mid': ['mid', 'intermediate', 'engineer', 'developer'],
            'senior': ['senior', 'sr', 'lead', 'principal', 'staff']
        }
        
        # Check for matches
        target_keywords = seniority_keywords.get(experience_level, [])
        matches = sum(1 for keyword in target_keywords if keyword in combined_text)
        
        if matches > 0:
            return 1.0
        
        # No clear match, give partial score
        return 0.5
    
    def _score_benefits(self, job: Dict[str, Any]) -> float:
        """
        Score based on benefits and perks.
        
        Returns:
            Score between 0 and 1
        """
        benefits = job.get('benefits', [])
        description = job.get('description', '').lower()
        
        # Common benefits to look for
        benefit_keywords = [
            'health insurance', '401k', 'retirement', 'stock options',
            'equity', 'pto', 'vacation', 'remote', 'flexible',
            'work-life balance', 'dental', 'vision', 'bonus'
        ]
        
        # Count how many benefits are mentioned
        benefit_count = 0
        for benefit in benefit_keywords:
            if benefit in description or benefit in str(benefits).lower():
                benefit_count += 1
        
        # Score based on number of benefits (max out at 6 benefits)
        return min(benefit_count / 6.0, 1.0)
