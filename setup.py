import os
from setuptools import setup, find_packages

setup(
    name="cab_booking",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "flask>=2.0.0",
    ],
    author="Cab Booking System",
    author_email="example@example.com",
    description="A cab booking system REST API",
    keywords="cab, taxi, booking, api",
    python_requires=">=3.6",
)
