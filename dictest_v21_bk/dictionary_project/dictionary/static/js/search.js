// Cache DOM elements and frequently used values
const elements = {
    searchInput: document.getElementById('search-input'),
    suggestionList: document.getElementById('suggestion-list'),
    keyboardIcon: document.getElementById('keyboard-icon'),
    miniKeyboard: document.getElementById('mini-keyboard')
  };
  
  // Configuration object for easy adjustments
  const config = {
    minQueryLength: 3,
    debounceDelay: 300,
    maxSuggestions: 10,
    highlightClass: 'highlight'
  };
  
  class SearchManager {
    constructor(elements, config) {
      this.elements = elements;
      this.config = config;
      this.isKeyboardVisible = false;
      this.previousQuery = '';
      this.suggestionCache = new Map();
      
      this.init();
    }
  
    init() {
      this.setupEventListeners();
    }
  
    setupEventListeners() {
      // Debounced input handler
      this.elements.searchInput.addEventListener('input', 
        this.debounce(this.handleInput.bind(this), this.config.debounceDelay)
      );
  
      // Click handlers
      document.addEventListener('click', this.handleDocumentClick.bind(this));
      this.elements.miniKeyboard.addEventListener('click', this.handleKeyboardClick.bind(this));
      this.elements.keyboardIcon.addEventListener('click', this.toggleKeyboard.bind(this));
  
      // Keyboard navigation for suggestions
      this.elements.searchInput.addEventListener('keydown', this.handleKeyboardNavigation.bind(this));
    }
  
    async handleInput() {
      const query = this.elements.searchInput.value.trim().toLowerCase();
      
      if (query.length < this.config.minQueryLength || query === this.previousQuery) {
        this.hideSuggestions();
        return;
      }
  
      this.previousQuery = query;
  
      if (this.suggestionCache.has(query)) {
        this.displaySuggestions(this.suggestionCache.get(query), query);
        return;
      }
  
      try {
        const suggestions = await this.fetchSuggestions(query);
        const sortedSuggestions = this.sortSuggestions(suggestions, query);
        this.suggestionCache.set(query, sortedSuggestions);
        this.displaySuggestions(sortedSuggestions, query);
      } catch (error) {
        console.error("Error fetching suggestions:", error);
        this.hideSuggestions();
      }
    }
  
    sortSuggestions(suggestions, query) {
        return suggestions
          .map(suggestion => ({
            ...suggestion,
            score: this.calculateRelevanceScore(suggestion.word.toLowerCase(), query),
          }))
          .sort((a, b) => b.score - a.score || a.word.localeCompare(b.word));
      }
      
  
    calculateRelevanceScore(word, query) {
        let score = 0;
      
        // Exact match
        if (word === query) {
          score += 3000;
        }
        // Exact prefix match
        else if (word.startsWith(query)) {
          score += 2000;
          score += (100 - word.length); // Favor shorter words
        }
        // Contains query
        else if (word.includes(query)) {
          score += 500; // Higher weight for inclusion
          if (word.includes(' ' + query)) {
            score += 250; // Favor matches at word boundaries
          }
        }
      
        // Bonus for words containing a hyphen if query matches one part
        if (word.includes('-') && word.split('-').some(part => part === query)) {
          score += 100;
        }
      
        return score;
      }
      
  
    async fetchSuggestions(query) {
      const encoded = encodeURIComponent(query);
      const response = await fetch(`/search/suggestions?q=${encoded}`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    }
  
    displaySuggestions(suggestions, query) {
      const fragment = document.createDocumentFragment();
  
      suggestions.forEach(suggestion => {
        const div = document.createElement('div');
        div.className = 'list-group-item';
        
        // Highlight the matching prefix if it exists
        const highlightedText = this.highlightPrefix(suggestion.word, query);
        div.innerHTML = highlightedText;
  
        // Add a subtle indicator of match type (optional)
        if (suggestion.word.toLowerCase().startsWith(query)) {
          div.classList.add('prefix-match');
        }
  
        div.addEventListener('click', () => {
          this.selectSuggestion(suggestion.word);
        });
  
        fragment.appendChild(div);
      });
  
      this.elements.suggestionList.innerHTML = '';
      this.elements.suggestionList.appendChild(fragment);
      this.elements.suggestionList.style.display = 'block';
    }
  
    highlightPrefix(text, query) {
      const lowerText = text.toLowerCase();
      const lowerQuery = query.toLowerCase();
      
      if (lowerText.startsWith(lowerQuery)) {
        // Highlight prefix match
        return `<span class="${this.config.highlightClass}">${text.slice(0, query.length)}</span>${text.slice(query.length)}`;
      } else {
        // Highlight all occurrences for non-prefix matches
        const regex = new RegExp(`(${query})`, 'gi');
        return text.replace(regex, `<span class="${this.config.highlightClass}">$1</span>`);
      }
    }
  
    // ... rest of the methods remain the same as in previous version ...
    selectSuggestion(text) {
      this.elements.searchInput.value = text;
      this.hideSuggestions();
      this.elements.searchInput.focus();
    }
  
    handleKeyboardNavigation(event) {
      const suggestions = this.elements.suggestionList.children;
      const currentIndex = Array.from(suggestions).findIndex(el => el.classList.contains('active'));
  
      switch(event.key) {
        case 'ArrowDown':
        case 'ArrowUp':
          event.preventDefault();
          this.navigateSuggestions(event.key === 'ArrowDown' ? 1 : -1, currentIndex, suggestions);
          break;
        case 'Enter':
          if (currentIndex >= 0) {
            event.preventDefault();
            this.selectSuggestion(suggestions[currentIndex].textContent);
          }
          break;
        case 'Escape':
          this.hideSuggestions();
          break;
      }
    }
  
    navigateSuggestions(direction, currentIndex, suggestions) {
      if (suggestions.length === 0) return;
  
      let newIndex = currentIndex + direction;
      if (newIndex < 0) newIndex = suggestions.length - 1;
      if (newIndex >= suggestions.length) newIndex = 0;
  
      Array.from(suggestions).forEach((el, i) => {
        el.classList.toggle('active', i === newIndex);
      });
    }
  
    handleKeyboardClick(event) {
      if (!event.target.classList.contains('char-btn')) return;
  
      const char = event.target.textContent;
      const input = this.elements.searchInput;
      const cursorPos = input.selectionStart;
  
      input.value = input.value.slice(0, cursorPos) + char + input.value.slice(cursorPos);
      input.setSelectionRange(cursorPos + 1, cursorPos + 1);
      input.focus();
      
      input.dispatchEvent(new Event('input'));
    }
  
    handleDocumentClick(event) {
      const isOutside = !this.elements.searchInput.contains(event.target) && 
                       !this.elements.suggestionList.contains(event.target);
      
      if (isOutside && event.target !== this.elements.keyboardIcon) {
        this.hideSuggestions();
      }
    }
  
    toggleKeyboard() {
      this.isKeyboardVisible = !this.isKeyboardVisible;
      this.elements.miniKeyboard.style.display = this.isKeyboardVisible ? 'block' : 'none';
    }
  
    hideSuggestions() {
      this.elements.suggestionList.style.display = 'none';
      this.elements.suggestionList.innerHTML = '';
    }
  
    debounce(func, wait) {
      let timeout;
      return function executedFunction(...args) {
        const later = () => {
          clearTimeout(timeout);
          func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
      };
    }
  }
  
  // Initialize the search manager
  const searchManager = new SearchManager(elements, config);
  
  // Add some CSS for visual distinction
  const style = document.createElement('style');
  style.textContent = `
    .prefix-match {
      background-color: rgba(0, 123, 255, 0.05);
    }
    .highlight {
      background-color: rgba(255, 255, 0, 0.3);
      font-weight: bold;
    }
  `;
  document.head.appendChild(style);