#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TextAnalyzer CLI - Command Line Interface
Interfaccia a riga di comando per TextAnalyzer
"""

import sys
import os
sys.path.insert(0, '/home/martina/PycharmProjects/TextAnalyzer')

import argparse
from typing import Optional
from core.text_analyzer import TextAnalyzer


def analyze_text(text: str, output: Optional[str] = None, calibrate: bool = False):
    """Analizza un testo e stampa risultati"""
    print("🧠 TextAnalyzer CLI v3.0")
    print("=" * 70)

    # Initialize
    analyzer = TextAnalyzer(auto_calibrate=False, debug=False)

    # Calibrate if requested
    if calibrate:
        print("\n🎯 Calibrating system...")
        result = analyzer.calibrate()
        if result['success']:
            print(f"✅ Calibration successful!")
            print(f"   Threshold: {result['threshold']:.4f}")
            print(f"   F1-Score: {result['f1_score']:.4f}")
        else:
            print(f"❌ Calibration failed: {result['error']}")

    # Analyze
    print(f"\n📝 Analyzing text...")
    print(f"   Length: {len(text)} characters")
    print(f"   Words: {len(text.split())} words")

    try:
        result = analyzer.analyze(text)

        # Display results
        print("\n" + "=" * 70)
        print("📊 RESULTS")
        print("=" * 70)

        print(f"\n🧠 CLASSIFICAZIONE:")
        print(f"   {result.classification}")
        print(f"   🤖 AI Probability: {result.ai_probability:.4f}")
        print(f"   👤 Human Probability: {result.human_probability:.4f}")

        print(f"\n🎯 CONFIDENCE:")
        print(f"   Certainty Level: {result.certainty_level}")
        print(f"   Confidence Score: {result.confidence:.4f}")
        print(f"   ⏱️ Processing Time: {result.processing_time_ms:.2f}ms")

        print(f"\n💡 RECOMMENDATION:")
        print(f"   {result.recommendation}")

        print(f"\n👥 ANALYZERS:")
        for name, data in result.individual_results.items():
            if isinstance(data, dict) and 'ai_probability' in data:
                print(f"   • {name}: {data['ai_probability']:.4f}")

        # Export if requested
        if output:
            analyzer.export_result(result, output)
            print(f"\n💾 Results exported to: {output}")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return 1

    return 0


def analyze_file(filepath: str, output: Optional[str] = None, calibrate: bool = False):
    """Analizza un file di testo"""
    if not os.path.exists(filepath):
        print(f"❌ Error: File '{filepath}' not found")
        return 1

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()
    except Exception as e:
        print(f"❌ Error reading file: {str(e)}")
        return 1

    print(f"📂 Analyzing file: {filepath}")

    if not output:
        output = f"{os.path.splitext(filepath)[0]}_analysis.json"

    return analyze_text(text, output, calibrate)


def batch_analyze(folder: str, output: Optional[str] = None, calibrate: bool = False):
    """Analizza tutti i file .txt in una directory"""
    if not os.path.exists(folder):
        print(f"❌ Error: Folder '{folder}' not found")
        return 1

    # Find txt files
    txt_files = [f for f in os.listdir(folder) if f.endswith('.txt')]
    if not txt_files:
        print(f"❌ Error: No .txt files found in '{folder}'")
        return 1

    print(f"📁 Found {len(txt_files)} .txt files in {folder}")

    analyzer = TextAnalyzer(auto_calibrate=False, debug=False)

    if calibrate:
        print("\n🎯 Calibrating system...")
        result = analyzer.calibrate()
        if result['success']:
            print(f"✅ Calibration successful!")

    results = []
    for i, filename in enumerate(txt_files, 1):
        filepath = os.path.join(folder, filename)
        print(f"\n[{i}/{len(txt_files)}] Analyzing {filename}...")

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()

            result = analyzer.analyze(text)
            results.append({
                'filename': filename,
                'classification': result.classification,
                'ai_probability': result.ai_probability,
                'confidence': result.confidence
            })

            print(f"   → {result.classification} (AI: {result.ai_probability:.3f})")

        except Exception as e:
            print(f"   ❌ Error: {str(e)}")

    # Export batch results
    if output:
        import json
        os.makedirs(os.path.dirname(output), exist_ok=True)
        with open(output, 'w', encoding='utf-8') as f:
            json.dump({
                'timestamp': analyzer.get_stats(),
                'results': results
            }, f, indent=2)

        print(f"\n💾 Batch results exported to: {output}")

    return 0


def show_stats():
    """Mostra statistiche sistema"""
    analyzer = TextAnalyzer()

    print("📊 TextAnalyzer Statistics")
    print("=" * 70)

    stats = analyzer.get_stats()

    print(f"\n🔧 System:")
    print(f"   Calibrated: {stats['is_calalyzed']}")
    print(f"   Threshold: {stats['calibration_threshold']}")
    print(f"   Cache: {stats['cache_size']} entries")

    print(f"\n📈 Usage:")
    print(f"   Total Analyses: {stats['total_analyses']}")
    print(f"   Avg Processing Time: {stats['avg_processing_time']:.2f}ms")
    print(f"   Avg Confidence: {stats['avg_confidence']:.3f}")

    print(f"\n🔍 Available Analyzers:")
    for name in stats['available_analyzers']:
        print(f"   • {name}")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='TextAnalyzer v3.0 - Ensemble AI Detection',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze a single text
  python3 cli.py --text "Your text here"

  # Analyze a file
  python3 cli.py --file input.txt --output results.json

  # Batch analyze a folder
  python3 cli.py --batch folder/ --output batch_results.json

  # Calibrate and analyze
  python3 cli.py --text "Your text" --calibrate

  # Show stats
  python3 cli.py --stats
        """
    )

    # Input options (mutually exclusive)
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('--text', type=str, help='Text to analyze')
    input_group.add_argument('--file', type=str, help='Text file to analyze')
    input_group.add_argument('--batch', type=str, help='Folder with .txt files to analyze')
    input_group.add_argument('--stats', action='store_true', help='Show system statistics')

    # Options
    parser.add_argument('--output', type=str, help='Output file for results (JSON)')
    parser.add_argument('--calibrate', action='store_true', help='Calibrate system before analyzing')
    parser.add_argument('--debug', action='store_true', help='Enable debug output')

    args = parser.parse_args()

    # Show stats
    if args.stats:
        show_stats()
        return 0

    # Analyze text
    if args.text:
        return analyze_text(args.text, args.output, args.calibrate)

    # Analyze file
    if args.file:
        return analyze_file(args.file, args.output, args.calibrate)

    # Batch analyze
    if args.batch:
        return batch_analyze(args.batch, args.output, args.calibrate)

    return 0


if __name__ == "__main__":
    sys.exit(main())
