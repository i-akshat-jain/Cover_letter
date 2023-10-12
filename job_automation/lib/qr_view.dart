import 'color_list.dart';
import 'package:flutter/material.dart';
import 'package:qr_flutter/qr_flutter.dart';

class CoverLetterView extends StatefulWidget {
  const CoverLetterView({super.key});

  @override
  State<CoverLetterView> createState() => _CoverLetterViewState();
}

class _CoverLetterViewState extends State<CoverLetterView> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
        body: ElevatedButton(onPressed: () {}, child: Text('Click to upload the Cover letter.')));
  }
}
