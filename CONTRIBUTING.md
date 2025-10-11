# Contributing to ByGone Spoofer

Thank you for your interest in contributing to ByGone Spoofer! This document provides guidelines for contributing to the project.

## Code of Conduct

- Be respectful and considerate of others
- Focus on constructive feedback
- Help maintain a welcoming environment
- Follow ethical guidelines

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](../../issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - System information (OS, Python version)
   - Error messages or logs

### Suggesting Features

1. Check existing [Issues](../../issues) for similar suggestions
2. Create a new issue with:
   - Clear description of the feature
   - Use case and benefits
   - Possible implementation approach

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/YourFeatureName
   ```
3. **Make your changes**
   - Follow existing code style
   - Add comments for complex logic
   - Update documentation if needed
4. **Test your changes**
   - Ensure code runs without errors
   - Test on Windows 10/11
   - Verify admin rights requirements
5. **Commit your changes**
   ```bash
   git commit -m "Add: Brief description of changes"
   ```
6. **Push to your fork**
   ```bash
   git push origin feature/YourFeatureName
   ```
7. **Open a Pull Request**
   - Describe what changes you made
   - Reference any related issues
   - Explain why the changes are needed

## Development Guidelines

### Code Style

- Follow PEP 8 Python style guide
- Use meaningful variable names
- Add docstrings to functions
- Keep functions focused and modular

### Documentation

- Update README.md for new features
- Add comments for complex logic
- Update CHANGELOG.md for your changes
- Include usage examples

### Testing

- Test on clean Windows installation
- Verify admin rights handling
- Check for edge cases
- Test reversal operations

## Areas for Contribution

### High Priority

- Bug fixes
- Performance improvements
- Documentation improvements
- Testing and validation
- Cross-platform support research

### Medium Priority

- New spoofing methods
- Enhanced safety features
- Better error handling
- UI/UX improvements
- Code optimization

### Low Priority

- Additional utilities
- Extended logging
- Configuration options
- Automation features

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/bygone-spoofer.git
cd bygone-spoofer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run in development mode:
```bash
python ByGoneSpoofer.py
```

## Questions?

- Open an issue for questions
- Review existing documentation in `/docs/`
- Check closed issues for similar questions

## Legal and Ethical Considerations

- Ensure contributions comply with applicable laws
- Do not include malicious code
- Respect terms of service
- Focus on educational/research purposes
- Include appropriate warnings and disclaimers

## Recognition

Contributors will be recognized in:
- README.md acknowledgments
- CHANGELOG.md for their contributions
- Project documentation

Thank you for contributing to ByGone Spoofer! 🎉

