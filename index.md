

<header>
  <h1>Multi-Class Sentiment Classification of Amazon Product Reviews Using DeBERTa</h1>
  <h2>ECEN 758 &mdash; Project: AmazonReviewFullClassification</h2>

  <div class="authors">
    <div>Riddhi Prakash Ghate, Praful Jeyaprakash, Sohanraj Rajanna, Carmelo Bustos </div>
    <div>Texas A&amp;M University</div>
  </div>
</header>

<div class="container">

  <!-- Abstract -->
  <h3>Abstract</h3>
  <p>
    Fine-grained sentiment classification of customer reviews presents significant challenges due to the subtle linguistic distinctions 
    between adjacent sentiment levels. This paper investigates the application of transformer-based models for five-class sentiment classification 
    of Amazon product reviews, where reviews are categorized from very negative to very positive based on one-star through five-star ratings. We conduct 
    comprehensive exploratory data analysis to identify rating-specific vocabulary patterns and systematically compare multiple architectures including 
    RNN, LSTM, and DeBERTa models. Our experimental results demonstrate that the DeBERTa transformer achieves the best performance with 60.64 percent overall 
    accuracy on a test dataset of 1250 reviews, representing a substantial improvement over RNN (19.42 percent) and LSTM (55.63 percent) baselines. Performance 
    analysis reveals clear disparities across sentiment classes: extreme sentiments achieve F1 scores of 0.71 for both very negative and very positive reviews, 
    while intermediate sentiments prove significantly more challenging with F1 scores ranging from 0.52 to 0.55, indicating performance differences of approximately 
    0.15 to 0.20. Confidence analysis shows that the model maintains a mean prediction confidence of 69.7 percent, with high-confidence predictions demonstrating 
    strong reliability through 110 correct versus only 14 incorrect classifications. These findings highlight both the effectiveness of transformer architectures 
    for sentiment analysis and the fundamental difficulty in distinguishing nuanced sentiment levels in the neutral range, providing insights for future work in 
    fine-grained opinion mining.
  </p>

  <!-- Overview / Motivation -->
  <h3>Overview</h3>
  <div class="two-col">
    <div>
      <h4>Problem</h4>
      <p>
        Online marketplaces like Amazon host millions of user reviews. Understanding this feedback at scale
        helps with product improvements, quality monitoring, and recommendation systems. However, subtle
        language differences between, say, 3-star and 4-star reviews make five-class sentiment prediction much
        more difficult than simple positive vs. negative classification.
      </p>
    </div>
  </div>






  <!-- Dataset -->
  <h3>Dataset</h3>
  <p>
    We use the Amazon Review Full dataset, which contains millions of reviews with 1&ndash;5-star ratings.
    For training, we sample 40,000 reviews with approximately equal numbers of each rating to reduce
    class imbalance while keeping training manageable. A separate test split of 1,250 reviews is used for
    final evaluation.
  </p>

  <h4>Text Characteristics</h4>
  <ul>
    <li>Average review length: ~80 words (max &approx; 260 words).</li>
    <li>Padding / truncation length: 260 tokens.</li>
    <li>Common content words (after stop-word removal): <em>book</em>, <em>good</em>, <em>like</em>, <em>great</em>, <em>just</em>, etc.</li>
    <li>Negative bigrams: <em>waste money</em>, <em>don’t buy</em>; positive bigrams: <em>highly recommend</em>, <em>great book</em>.</li>
  </ul>
<img width="1402" height="669" alt="image" src="https://github.com/user-attachments/assets/d9e5bb66-adf4-4327-af65-bd17a36d397b" />








  <!-- Methods -->
  <h3>Methods</h3>

  <h4>Data Preparation</h4>
  <ul>
    <li>Lowercasing of all text.</li>
    <li>Removal of HTML tags, URLs, emails, digits, and special characters.</li>
    <li>Whitespace normalization and basic repetition cleanup.</li>
    <li>Ratings kept as 1&ndash;5 labels (0-indexed only where required by libraries).</li>
    <li>Stratified train/validation splits (e.g., 80% / 20%) to preserve class balance.</li>
  </ul>

  <h4>Models Compared</h4>
  <ul>
    <li><strong>RNN baseline</strong>: simple recurrent model with BERT token embeddings, trained with Adam and
      cross-entropy loss.</li>
    <li><strong>LSTM</strong>: replaces RNN with LSTM layers, better handling long-range dependencies in reviews.</li>
    <li><strong>DeBERTa-v3-base</strong>: transformer model with disentangled attention and enhanced masked decoder;
      fine-tuned on our 40k-review subset using <code>AdamW</code>, a linear learning-rate scheduler, and 5 epochs
      of training (best checkpoint selected by validation loss).</li>
  </ul>













  <!-- Results -->
  <h3>Results</h3>

  <h4>Overall Performance</h4>
  <table class="metrics-table">
    <thead>
      <tr>
        <th>Model</th>
        <th>Test Accuracy</th>
        <th>Macro F1</th>
        <th>Notes</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>RNN</td>
        <td>19.42%</td>
        <td>&asymp;0.19</td>
        <td>Struggles across all classes.</td>
      </tr>
      <tr>
        <td>LSTM</td>
        <td>55.63%</td>
        <td>0.55</td>
        <td>Tighter confusion matrix; mistakes mostly between neighboring ratings.</td>
      </tr>
      <tr>
        <td><strong>DeBERTa-v3</strong></td>
        <td><strong>60.64%</strong></td>
        <td><strong>0.60</strong></td>
        <td>Best overall; particularly strong for extreme ratings (1★ &amp; 5★).</td>
      </tr>
    </tbody>
  </table>

  <h4>Per-Class Metrics (DeBERTa)</h4>
  <table class="metrics-table">
    <thead>
      <tr>
        <th>Class</th>
        <th>Rating</th>
        <th>Accuracy</th>
        <th>Precision</th>
        <th>Recall</th>
        <th>F1</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>0</td><td>1★ (very negative)</td><td>0.760</td><td>0.664</td><td>0.760</td><td>0.709</td>
      </tr>
      <tr>
        <td>1</td><td>2★ (negative)</td><td>0.516</td><td>0.520</td><td>0.516</td><td>0.518</td>
      </tr>
      <tr>
        <td>2</td><td>3★ (neutral)</td><td>0.472</td><td>0.593</td><td>0.472</td><td>0.526</td>
      </tr>
      <tr>
        <td>3</td><td>4★ (positive)</td><td>0.532</td><td>0.559</td><td>0.532</td><td>0.545</td>
      </tr>
      <tr>
        <td>4</td><td>5★ (very positive)</td><td>0.752</td><td>0.674</td><td>0.752</td><td>0.711</td>
      </tr>
    </tbody>
  </table>

  <p>
    As expected, reviews with very negative (1★) or very positive (5★) sentiment are easier to classify than
    intermediate classes. Most errors happen between adjacent ratings (e.g., 3★ vs. 4★), reflecting the
    nuanced language typical of mild reviews.
  </p>

  <h4>Confusion Matrix (DeBERTa)</h4>
  <ul>
    <img width="1182" height:auto alt="image" src="https://github.com/user-attachments/assets/a49c62f1-347e-43d4-aeac-5ea0c4df2891" />



















  <!-- Materials / Links -->
  <h3>Materials</h3>
  <div class="materials-grid">
    <div class="material-card">
      <div class="material-card-title">Code (GitHub):</div>
      <p>
        <a href="https://github.com/ECEN-758-Project-Team/AmazonReviewFullClassification" target="_blank">
          AmazonReviewFullClassification Repository
        </a>
      </p>
    </div>



