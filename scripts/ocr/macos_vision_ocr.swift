import Foundation
import CoreImage
import AppKit
import Vision

struct OCRAnnotation: Codable {
    let text: String
    let confidence: Double
    let bounding_box: [Double]
}

struct OCRResult: Codable {
    let filename: String
    let annotation_count: Int
    let full_text: String
    let annotations: [OCRAnnotation]
    let engine: String
}

enum OCRScriptError: Error {
    case missingInputPath
    case unreadableImage
}

func loadCGImage(from imageURL: URL) throws -> CGImage {
    guard let image = NSImage(contentsOf: imageURL) else {
        throw OCRScriptError.unreadableImage
    }
    var proposedRect = NSRect(origin: .zero, size: image.size)
    guard let cgImage = image.cgImage(forProposedRect: &proposedRect, context: nil, hints: nil) else {
        throw OCRScriptError.unreadableImage
    }
    return cgImage
}

func recognizeText(imageURL: URL) throws -> OCRResult {
    let cgImage = try loadCGImage(from: imageURL)
    let request = VNRecognizeTextRequest()
    request.recognitionLevel = .accurate
    request.usesLanguageCorrection = true

    let handler = VNImageRequestHandler(cgImage: cgImage, options: [:])
    try handler.perform([request])

    let observations = request.results ?? []
    let annotations: [OCRAnnotation] = observations.compactMap { observation in
        guard let candidate = observation.topCandidates(1).first else {
            return nil
        }
        let bbox = observation.boundingBox
        return OCRAnnotation(
            text: candidate.string,
            confidence: Double(candidate.confidence),
            bounding_box: [
                Double(bbox.origin.x),
                Double(bbox.origin.y),
                Double(bbox.size.width),
                Double(bbox.size.height),
            ]
        )
    }

    let fullText = annotations
        .map(\.text)
        .filter { !$0.isEmpty }
        .joined(separator: "\n")

    return OCRResult(
        filename: imageURL.lastPathComponent,
        annotation_count: annotations.count,
        full_text: fullText,
        annotations: annotations,
        engine: "swift_vision_fallback"
    )
}

do {
    guard CommandLine.arguments.count >= 2 else {
        throw OCRScriptError.missingInputPath
    }

    let inputPath = (CommandLine.arguments[1] as NSString).expandingTildeInPath
    let imageURL = URL(fileURLWithPath: inputPath)
    let result = try recognizeText(imageURL: imageURL)

    let encoder = JSONEncoder()
    let data = try encoder.encode(result)
    if let json = String(data: data, encoding: .utf8) {
        print(json)
    }
} catch OCRScriptError.missingInputPath {
    fputs("{\"error\":\"missing input path\"}\n", stderr)
    exit(1)
} catch OCRScriptError.unreadableImage {
    fputs("{\"error\":\"unable to read image\"}\n", stderr)
    exit(2)
} catch {
    let escaped = error.localizedDescription.replacingOccurrences(of: "\"", with: "\\\"")
    fputs("{\"error\":\"\(escaped)\"}\n", stderr)
    exit(3)
}
