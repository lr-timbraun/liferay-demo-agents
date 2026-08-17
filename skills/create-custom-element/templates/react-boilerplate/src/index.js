/* global Liferay */
import React from 'react';
import { createRoot } from 'react-dom/client';

const App = () => {
    return (
        <div className="react-boilerplate-container">
            <div className="card">
                <div className="card-body">
                    <h1 className="card-title">React Custom Element Boilerplate</h1>
                    <p className="card-text">
                        This is a gold-standard React custom-element client extension template. It is fully integrated with Liferay's styling tokens and security systems.
                    </p>
                </div>
            </div>
        </div>
    );
};

class ReactBoilerplateElement extends HTMLElement {
    connectedCallback() {
        if (!this.root) {
            // Mount React virtual DOM directly inside this web component's custom tag wrapper
            this.root = createRoot(this);
        }
        this.root.render(<App />);
    }

    disconnectedCallback() {
        if (this.root) {
            // Cleanly unmount React root when element is removed from DOM to prevent memory leaks
            this.root.unmount();
            this.root = null;
        }
    }
}

const ELEMENT_ID = 'react-custom-element-boilerplate';
if (!customElements.get(ELEMENT_ID)) {
    customElements.define(ELEMENT_ID, ReactBoilerplateElement);
}
